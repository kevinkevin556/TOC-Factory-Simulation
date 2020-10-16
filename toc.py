from math import inf
from random import randint
from statistics import stdev

import pandas as pd
import plotly.express as px


# Functions

def production(random_func, *args, **kwargs):
    def output():
        return random_func(*args, **kwargs)
    return output

def dice(min=1, max=6):
    return production(randint, min, max)


# Classes

class Machine:
    def __init__(self, output, buffer=0):
        self.output = output        # 機器產出 (int or a function)
        self.init_buffer = buffer   # 初始緩衝區存貨
        self.buffer = buffer        # 目前緩衝區存貨
        
    
    def info(self, init_buffer=False, mode="print"):
        if init_buffer:
            info = "(buffer, initial buffer) = ({}, {})".format(self.buffer, self.init_buffer)
        else:
            info = "buffer = {}".format(self.buffer)
        
        if mode == "print":
            print(info)
        if mode == "return":
            return info


    def produce(self, *args, **kwargs):
        if callable(self.output):
            output = self.output(*args, **kwargs)
        else:
            output = self.output

        # self.buffer 是機器目前緩衝區內的存貨
        # output 代表機器的生產量
        buffer = self.buffer
        output = min(output, buffer)
        self.buffer -= output
        return output
    

class Factory:
    def __init__(self, n=0, output=None, buffer=None):
        self.machines = [Machine(output, buffer) for i in range(n)]      # 工廠內機器
        if n > 0:
            self.machines[0] = Machine(output, 0)                            # 第一部機器沒有緩衝區
            self.wip = sum([self.machines[i].buffer for i in range(1, n)])   # 工廠目前存貨總數
        else:
            self.wip = None

    def info(self, init_buffer=False, mode="print"):
        info = ""
        for i in range(len(self.machines)):
            machine = self.machines[i]
            if i != 0:
                info += "Machine {} ".format(i) + machine.info(init_buffer, mode="return")
                if i != len(self.machines)-1:
                    info += "\n"
            else:
                info += "Machine 0 No Buffer \n"
        
        if mode == "print":
            print(info)
        if mode == "return":
            return info


    def add(self, machine, n=1):
        for i in range(n):
            self.machines.append(machine)


    def init_machines(self):
        for machine in self.machines:
            machine.buffer = machine.init_buffer


    def simulation(self, n_sim=50, day=10):
        simulation = Simulation(self)
        simulation.run(factory=None, n_sim=n_sim, day=day)
        return simulation


    def start(self, input=inf, restart=True):
        if restart:
            self.init_machines()

        # wip 代表機器間(傳遞的)存貨
        # machine.buffer 代表目前那台機器緩衝區的存貨量
        # machine.produce() 代表透過那台機器生產，會回傳一個數字(生產量)
        #
        # 在下面的 for 迴圈中，逐一遍歷每台機器，
        # 完成生產與緩衝區補存貨的動作。
        wip = input
        for machine in self.machines:
            machine.buffer += wip
            wip = machine.produce()

        output = wip
        self.wip = sum([self.machines[i].buffer for i in range(1, len(self.machines))])
        return output
    

class Simulation:
    def __init__(self, factory):
        self.factory = factory
        self.output = None
        self.simulation_recording = None
        
    
    def run(self, factory=None, n_sim=50, day=10):
        if factory is not None:
            self.factory = factory
        else:
            factory = self.factory

        output = []
        wip = []
        recording_output = []
        recording_wip = []
        recording_round = []
        for i in range(1, n_sim+1):
            factory.init_machines()
            total_output = sum([factory.start(restart=False) for j in range(day)])
            output.append(total_output)
            wip.append(factory.wip)

            recording_output += output
            recording_wip += wip
            recording_round += [i for _ in output]
            
        self.simulation_recording = pd.DataFrame({
            "output": recording_output,
            "wip": recording_wip,
            "round": recording_round})
        self.output = output
        self.wip = wip
        return output, wip
    

    def visualize(self, item=["output", "wip"], play_speed=10):
        if self.simulation_recording is None:
            self.run()
        
        df = self.simulation_recording
        output = df[df["round"]==max(df["round"])].output.tolist()
        wip = df[df["round"]==max(df["round"])].wip.tolist()

        if "output" == item or "output" in item:
            fig = px.histogram(df, x="output", 
                                animation_frame="round",
                                nbins = int(max(output))+1, 
                                range_x = (min(output)-2*stdev(output), max(output)+2*stdev(output)),
                                range_y = (0, output.count(max(output, key=output.count))*1.1),
                                color_discrete_sequence = [px.colors.qualitative.Plotly[0]],
                                opacity = 0.8)
            
            fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = play_speed
            fig.layout.sliders[0]['active'] = len(fig.frames) - 1
            fig.update_traces(x=fig.frames[-1].data[0].x)
            
            fig.show()
        
        if "wip" == item or "wip" in item:
            fig = px.histogram(df, x="wip", 
                                animation_frame="round",
                                nbins = int(max(wip))+1, 
                                range_x = (min(wip)-2*stdev(wip), max(wip)+2*stdev(wip)),
                                range_y = (0, wip.count(max(wip, key=wip.count))*1.1),
                                color_discrete_sequence = [px.colors.qualitative.Plotly[1]],
                                opacity = 0.8)
            
            fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = play_speed
            fig.layout.sliders[0]['active'] = len(fig.frames) - 1
            fig.update_traces(x=fig.frames[-1].data[0].x)
            
            fig.show()