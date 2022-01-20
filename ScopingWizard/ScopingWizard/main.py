# encoding: utf-8

def stepLoad_onupdate(step):
    # 获得ACT向导界面的输入值
    fixLoc = step.Properties["fixLoc"].Value
    pressLoc = step.Properties["pressLoc"].Value
    pressVal = step.Properties["pressVal"].Value
    analysis = Model.Analyses[0]
    # 加载固定约束
    fixSup = analysis.AddFixedSupport()
    fixSup.Location = fixLoc
    # 加载压力载荷
    pressLoad = analysis.AddPressure()
    pressLoad.Location = pressLoc
    import units
    curPressUnit = units.GetCurrentCompactUnitString("Pressure")
    pressQuntity = Quantity("%s [%s]" % (pressVal, curPressUnit))
    pressLoad.Magnitude.Output.DiscreteValues = [pressQuntity]
    Model.Solve()
    # 后处理操作
    solution = analysis.Solution
    misesResult = solution.AddEquivalentStress()
    misesResult.EvaluateAllResults()    