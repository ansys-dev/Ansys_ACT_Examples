# encoding: utf-8

def GetTabularData(table):
    from collections import defaultdict
    tabularData = defaultdict(list)
    for prop in table.AllDescendants:
        for row in range(table.RowCount):
            table.ActiveRow = row
            tabularData[prop.Name].append(prop.Value)
    return tabularData


def GenerateFreqHtmlContent(freqData, accData):
    tableTemplate = r"""<body>
    <p>Table1. Frequency vs. Acceleration</p>
    <table border="1">
      <tr><th width: 200px;>Frequency [HZ]</th>
        <th width: 240px;>Acceleration [g's]</th></tr>
      {tableData}
    </table></body>"""
    dataTemplate = r"""<tr><td align="center">{freq}</td>
        <td align="center">{acc}</td></tr>"""
    content = ""
    for freqVal, accVal in zip(freqData, accData):
        content += dataTemplate.format(freq=freqVal, acc=accVal)
    return tableTemplate.format(tableData=content)


def onFreqTableA_Apply(step, table):
    freqHtml = step.UserInterface.GetComponent("FreqHtml")
    if table.IsValid:
        tabularData = GetTabularData(table)
        tableContent = GenerateFreqHtmlContent(
            tabularData["freqA"], tabularData["accA"])
        freqHtml.SetHtmlContent(tableContent)
        freqHtml.Refresh()


def onFreqTableB_Apply(step, table):
    table.Controller.onapply(step, table)
    if table.IsValid:
        tabularData = GetTabularData(table)
        freqChart = step.UserInterface.GetComponent("FreqChart")
        freqChart.Title("Frequency vs. Acceleration")
        freqChart.XLabel("Frequency (HZ)")
        freqChart.YLabel("Acceleration (g's)")
        freqChart.ShowLegend(False)
        freqChart.Plot(tabularData["freqB"], tabularData["accB"])
        freqChart.Refresh()


def CreateMaterial(engData, name, density, strength, *elas):
    mat = engData.CreateMaterial(Name=name)
    mat.CreateProperty(Name="Density").SetData(Variables=["Density"],
    Values=[["%s [kg m^-3]"%density]])
    mat.CreateProperty(Name="Tensile Yield Strength").SetData(
        Variables=["Tensile Yield Strength"], Values=[["%s [Pa]"%strength]])
    elasProp = mat.CreateProperty(Name="Elasticity", Behavior="Isotropic")
    elasProp.SetData(Variables=["Young's Modulus"], Values=[["%s [Pa]"%elas[0]]])
    elasProp.SetData(Variables=["Poisson's Ratio"], Values=[["%s"%elas[1]]])


def onTableStepInit(step):
    matPropsDict = {"AISI 6150 Steel": [7861.1, 5.15e8, 2.078e11, 0.29],
                "Type 40 Gray Cast Iron": [7149.7, 2.94e8, 1.22e11, 0.29],
                "Type 302 Stainless Steel": [7861.1, 2.4e8, 2.048e11, 0.25]}
    matTable = step.Properties["matTable"]
    for matName in matPropsDict:
        matTable.AddRow()
        propData = matPropsDict[matName]
        matTable.Properties["matName"].Value = matName
        propList = ["density", "tensile","young", "poisson"]
        for index, propName in enumerate(propList):
            matTable.Properties[propName].Value = propData[index]
        # 保存表格当前行的数据
        matTable.SaveActiveRow()
        

def onTableStepUpdate(step):
    # 创建工程材料库系统
    engSys = GetTemplate(TemplateName="EngData").CreateSystem()
    projectName = step.Properties["projectName"].Value
    engSys.DisplayText = projectName
    # 获得Engineering Data数据容器
    engData = engSys.GetContainer(ComponentName="Engineering Data")
    matTableData = GetTabularData(step.Properties["matTable"])
    for name, density, strength, young, poi in zip(matTableData["matName"],
                                            matTableData["density"],
                                            matTableData["tensile"],
                                            matTableData["young"],
                                            matTableData["poisson"]):
        CreateMaterial(engData, name, density, strength, young, poi)
    