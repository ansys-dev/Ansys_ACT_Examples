# encoding: utf-8
clr.AddReference("Ans.UI")
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
from Ansys.UI import UIManager
from Ansys.UI.Toolkit import (MessageBox, 
                        MessageBoxType,
                        MessageBoxButtons,
                        Window)
from Ansys.ACT.Interfaces.UserInterface import ButtonPositionType

# Initialization for the custom buttons component
def onRefresh_ButtonStep(step):
    # Setup the buttons component
    btnComp = step.UserInterface.GetComponent("CustomButton")
    #@Params -- name: str, caption: str, position: ButtonPositionType -> None
    btnComp.AddButton("customBtn", "Custom Button", ButtonPositionType.Center)
    # Hook up the click event function for buttons
    btnComp.ButtonClicked += onClick_CustomButton

# The callback function that executes after the button is clicked    
def onClick_CustomButton(component, buttonArgs):
    ExtAPI.Log.WriteMessage("Custom Button Clicked!")
    MessageBox.Show(Window.ActiveWindow, "Custom Button Clicked!",
        "Ansys ACT", MessageBoxType.Info, MessageBoxButtons.OK)

    
def onUpdate_ButtonStep(step):
    pass
    
def onReset_ButtonStep(step):
    pass