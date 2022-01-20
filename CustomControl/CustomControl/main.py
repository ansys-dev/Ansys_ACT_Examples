# encoding: utf-8
clr.AddReference("Ans.UI")
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
from Ansys.UI import UIManager
from Ansys.UI.Toolkit import (MessageBox, 
                        MessageBoxType,
                        MessageBoxButtons,
                        Window)
from Ansys.ACT.Core.UI import (UIFactories,
                        LayoutDefinition)
from Ansys.ACT.Core.XmlDataModel.UI import Layout
from Ansys.ACT.Interfaces.UserInterface import (ButtonPositionType,
                                    ComponentLengthType)
from Ansys.ACT.Core.UI.HTMLRenderer import (PropertiesWebObject, 
                                    PropertyWebObject,
                                    CallbackWebObject)
from System.Collections.Generic import List

import os

dialogComp = None
optCnt = 0

# Initialization for the custom buttons component
def onRefresh_ButtonStep(step):
    # Setup the buttons component
    btnComp = step.UserInterface.GetComponent("CustomButton")
    #@Params -- name: str, caption: str, position: ButtonPositionType -> None
    btnComp.AddButton("customBtn", "Custom Button", ButtonPositionType.Center)
    # Hook up the click event function for buttons
    btnComp.ButtonClicked += onClick_CustomButton
    
    propsComp = step.UserInterface.GetComponent("Properties")
    userCtrl = step.Properties["userCtrl"]
    userCtrlData = GetPropWebObjWithName(propsComp, "userCtrl")
    
    def BoundApplyCallback(s, e):
        userCtrl.Apply()
        
    userCtrlData.Buttons.Add("Refresh")
    userCtrlData.ButtonClicked = CallbackWebObject("ButtonClicked", propsComp.Container)
    userCtrlData.ButtonClicked.Called += BoundApplyCallback
    propsComp.UpdateData()
    propsComp.Refresh()

def onApplyUserCtrl(step, prop):
    ExtAPI.Log.WriteMessage("Clicked")
    global optCnt
    prop.Options.Add("option{}".format(optCnt))
    optCnt += 1
    propsComp = step.UserInterface.GetComponent("Properties")
    propsComp.UpdateData()
    propsComp.Refresh()

def GetPropWebObjWithName(propsComp, propName):
    stack = []
    stack.append(propsComp.GetData[PropertiesWebObject]().RootProperty)
    while stack:
        for propWebObj in stack.pop().Properties:
            if propWebObj.RefSimProperty.Name == propName:
                return propWebObj
            if propWebObj.Properties:
                stack.append(propWebObj)

# The callback function that executes after the button is clicked    
def onClick_CustomButton(component, buttonArgs):
    ExtAPI.Log.WriteMessage("Custom Button Clicked!")

def onUpdate_ButtonStep(step):
    pass
    
def onReset_ButtonStep(step):
    pass