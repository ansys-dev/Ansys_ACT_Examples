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
from System.Collections.Generic import List

import os

dialogComp = None

# Initialization for the custom buttons component
def onRefresh_ButtonStep(step):
    # Setup the buttons component
    btnComp = step.UserInterface.GetComponent("CustomButton")
    #@Params -- name: str, caption: str, position: ButtonPositionType -> None
    btnComp.AddButton("customBtn", "Custom Button", ButtonPositionType.Center)
    # Hook up the click event function for buttons
    btnComp.ButtonClicked += onClick_CustomButton
    
    panelComp = step.UserInterface.Panel
    global dialogComp
    dialogComp = panelComp.CreateDialog("CustomDialog", "Custom Dialog", 400, 150)
    layoutDef = UIFactories.GetLayoutDefinitionByName("DialogLayout@ExtCustomDialog")
    dialogComp.SetLayout(layoutDef)
    imgComp = dialogComp.GetComponent("Image")
    btnsComp = dialogComp.GetComponent("Buttons")
    txtComp = dialogComp.GetComponent("Text")
    txtComp.SetHtmlContent("用户自定义按钮")
    extDir = ExtAPI.ExtensionManager.CurrentExtension.InstallDir
    imgComp.Source = os.path.join(extDir, "images", "information.png")
    btnsComp.AddButton("okBtn", "Ok", ButtonPositionType.Center)
    btnsComp.AddButton("cancelBtn", "Cancel", ButtonPositionType.Center)
    btnsComp.ButtonClicked += onClick_DialogButton
    dialogComp.RefreshBaseComponent()
    dialogComp.Refresh()


class CustomACTLayout:

    def __init__(self):
        layout = Layout(Components=List[Component]())
        self.__layoutDef = LayoutDefinition(Layout=layout)

    def AddComponent(self, component):
        self.__layoutDef.Layout.Components.Add(Component(**component))

    def AddComponents(self, components):
        for component in components:
            self.AddComponent(component)

    def GetLayoutDef(self):
        return self.__layoutDef

class DialogTypeEnum:
    Warning = 0
    Error = 1
    AttentionRequired = 2
    Informational = 3


class CustomACTDialog:

    def __init__(self, parent, name, title, width=400, height=150):
        self._dialogComp = parent.CreateDialog(title, name, width, height)
        layoutDef = self.GetLayout().GetLayoutDef()
        self._dialogComp.SetLayout(layoutDef)
        self._imageComp = self._dialogComp.GetComponent("Image")
        self._txtComp = self._dialogComp.GetComponent("Text")
        self._btnsComp = self._dialogComp.GetComponent("Buttons")
        
        
    def GetLayout(self):
        layout = CustomACTLayout()
        layout.AddComponents([{
                "Name":"Image", 
                "ComponentType":"imageComponent",
                "Topoffset": 10, 
                "BottomAttachment":"Buttons",
                "Leftoffset": 20, 
                "RightAttachment": "Text",
                "WidthType": ComponentLengthType.Percentage, 
                "WidthValue": 20,
                "HeightType": ComponentLengthType.Fixed, 
                "HeightValue": 64
            },
            {
                "Name": "Text", 
                "ComponentType": "htmlComponent",
                "Topoffset": 20, 
                "BottomAttachment": "Buttons",
                "LeftAttachment": "Image", 
                "WidthType": ComponentLengthType.Percentage,
                "WidthValue": 80,
                "HeightType": ComponentLengthType.FitToContent,
                "HeightValue": 50,
                "MinHeight":50
            },
            {
                "Name"="Buttons",
                "ComponentType": "buttonsComponent",
                "TopAttachment" : "Text",
                "LeftAttachment":"Image",
                "WidthType" : ComponentLengthType.Percentage,
                "WidthValue": 100,
                "HeightType": ComponentLengthType.Percentage,
                "HeightValue": 50
            }])
        return layout
    
    def SetMessage(self, message):
        self._txtComp.Content = message
        self._txtComp.Refresh()
    
    def SetType(self, type_):
        mapper = ["warning", "error", "attn_required", "informational"]
        self._imageComp.Source = "images/" + mapper[type_] + ".png"
        self._imageComp.Center = True
        self._imageComp.Refresh()
        
    def SetCallback(self, func):
        pass
    
    def AddButton(self, name, caption):
        self._btnsComp.AddButton(name, caption, ButtonPositionType.Center, True, False)
        self._btnsComp.Show()
        self._btnsComp.Refresh()
        
    def Hide(self):
        self._dialogComp.Hide()
        
    def Show(self):
        self._dialogComp.Show()


# The callback function that executes after the button is clicked    
def onClick_CustomButton(component, buttonArgs):
    ExtAPI.Log.WriteMessage("Custom Button Clicked!")
    dialogComp.Show()

def onClick_DialogButton(component, buttonArgs):
    if buttonArgs.ButtonName == "okBtn":
        MessageBox.Show(Window.ActiveWindow, "Dialog Ok Button Clicked!",
            "Ansys ACT", MessageBoxType.Info, MessageBoxButtons.OK)
        dialogComp.Hide()
    else:
        dialogComp.Hide()
    
def onUpdate_ButtonStep(step):
    pass
    
def onReset_ButtonStep(step):
    pass