# TOC-Factory-Simulation

這個簡單的專案透過 Python 實作基於制約理論的工廠生產模擬, 並提供模擬結果的視覺呈現。

其中主要檔案有：

* `toc.py`: 主要程式 (內含：機器、工廠、模擬類別)
* [`factory_simulation.ipynb`](https://nbviewer.jupyter.org/github/kevinkevin556/TOC-Factory-Simulation/blob/main/factory_simulation.ipynb): 作業管理 Self-Study Assignment #A 題目與生產模擬結果 


![Simulation_demo](https://i.imgur.com/hD5shyW.gif)

## 安裝

首先下載此 repository。接著開啟一個終端機 (terminal/commandline tool)，切換到下載後 repo 的目錄下，
輸入以下指令以安裝(或更新)相依的套件。

```Console
pip install -r requirements.txt
```

或者手動安裝需要的套件：

```Console
pip install plotly
pip install pandas
```

最後將工作目錄設為此 repo 的資料夾(包含`toc.py`)，就可以開始使用了。

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

## 參考連結

1. [NTU 109-1 商研所 作業管理](http://guo.ba.ntu.edu.tw/f4.htm)
2. [The Goal: A Process of Ongoing Improvement](https://www.amazon.com/Goal-Process-Ongoing-Improvement/dp/0884271951)
3. [Goldratt Marketing: Theory of Constraints](https://www.toc-goldratt.com/en)

## 開源協議

[MIT](https://opensource.org/licenses/MIT) © Kevin Hong
