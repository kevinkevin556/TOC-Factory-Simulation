# TOC-Factory-Simualtion

基於制約理論的工廠生產模擬。

## 安裝

首先下載此 repository。接著開啟一個終端機 (terminal/commandline tool)，切換到下載後 repo 的目錄下，
輸入以下指令以安裝(或更新)相依的套件。

```Console
pip install -r requirements.txt
```

將工作目錄設為此 repo 的資料夾(包含`toc.py`)，就可以開始使用了。

## 範例程式

```Python
from statistics import mean
from random import randint
from toc import Machine, Factory, Simulation, dice

factory = Factory(n=5, output=dice(), buffer=4)   # 設定一條裝設 5 部機器的產線，機器隨機生產 1-6 個存貨，每部機器前(不包含首部機器)緩衝區堆存 4 份存貨
sim = factory.simulation(n_sim=50, day=10)        # 模擬 50 次生產情形，每次生產連續完成 10 輪 (10 天)
sim.visualize()                                   # 呈現模擬結果

print(mean(sim.output))                           # 模擬 50 次平均總產出
print(mean(sim.wip))                              # 模擬 50 次平均產線上存貨
```
