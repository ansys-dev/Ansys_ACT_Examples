# encoding: utf-8
import math
import random

chartFuncDict = {}

def register(key):
    def decorate(func):
        chartFuncDict[key] = func
        return func
    return decorate
        
@register("Line")
def CreateLineChart(chart):
    chart.Title("Line Chart")    
    chart.XLabel("XLabel")
    chart.YLabel("YLabel")
    chart.XTickFormat("f")
    chart.YTickFormat("0.2f")
    xValues, y1Values, y2Values = [], [], []
    for i in range(0, 101):
        xValues.append(i * 0.1)
        y1Values.append(math.sin(i * 0.1))
        y2Values.append(math.cos(i * 0.1))
    chart.Plot(xValues, y1Values, key="y = sin(x)", color="c")
    chart.Plot(xValues, y2Values, key="y = cos(x)", color="r")    
    
@register("Pie")    
def CreatePieChart(chart):
    chart.Title("Pie Chart")
    chart.Pie([35, 32, 20, 13], ["Python", "Java", "C#", "C++"])

@register("Bubble")     
def CreateBubbleChart(chart):
    chart.Title("Bubble Chart")
    chart.XTickFormat(".2f")
    chart.YTickFormat(".2f")
    keys = ["Group1", "Group2", "Group3", "Group4", "Group5"]
    colors = ["#BB3333", "#33BB33", "#3333BB", "#BBBB33", "#BB33BB"]
    shapes = ["circle", "cross", "triangle-up", "diamond", "square"]
    for i in range(0, 5): 
        xValues, yValues = [], []
        sizeValues, shapeValues = [], []
        for j in range(0, 50):  
            rad = i + random.random() * 2 - 1
            angle = random.random() * 2 * math.pi
            xValues.append(math.cos(angle) * rad)
            yValues.append(math.sin(angle) * rad)
            sizeValues.append(round(random.random() * 100) / 100.0)
            shapeValues.append(shapes[i])
        chart.Bubble(xValues, yValues, sizeValues,shapeValues, key=keys[i], 
            color=colors[i])

@register("Bar")    
def CreateBarChart(chart):
    chart.Title("Bar Chart")
    chart.Bar(["Python", "Java", "C#", "C++"], [35, 32, 20, 13])

@register("LineBar") 
def CreateLineBarChart(chart):
    chart.Title("Line Bar Chart")
    chart.ShowLegend(False)
    chart.Plot([-1, 0, 1, 2, 3, 4],  [4, 10, 12, 6, 5, 10], key="Line", color='g')
    chart.Bar([-1, 0, 1, 2, 3, 4],  [10, 20, 30, 10, 5, 20], key="Bar")

def changeChartType(step, prop):
    # 获取定义的图表组件实例对象
    chart = step.UserInterface.GetComponent("Chart")
    chart.ClearData()
    chart.Reset()
    retFunc = chartFuncDict.get(prop.Value, None)
    if retFunc: retFunc(chart)
    chart.Refresh()

def onChartStepUpdate(step):
    pass
    
def onChartStepReset(step):
    pass
    
def onGraphStepRefresh(step):
    lineChart = step.UserInterface.GetComponent("LineChart")
    CreateLineChart(lineChart)
    barChart = step.UserInterface.GetComponent("BarChart")
    CreateBarChart(barChart)    
    pieChart = step.UserInterface.GetComponent("PieChart")
    CreatePieChart(pieChart)    
    lineBarChart = step.UserInterface.GetComponent("LineBarChart")
    CreateLineBarChart(lineBarChart)
    bubbleChart = step.UserInterface.GetComponent("BubbleChart")
    CreateBubbleChart(bubbleChart)    
        
def onGraphStepUpdate(step):
    pass