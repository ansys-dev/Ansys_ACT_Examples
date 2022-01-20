# -*- coding: utf-8 -*-
import clr
import System
import sys
import os

clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ansys.ACT.Core")

from Ansys.UI.Toolkit import *

from Ansys.ACT.Core.UI.HTMLRenderer import (PropertiesWebObject,
                                            PropertyWebObject,
                                            CallbackWebObject)


class FileSaveObj:

    def __init__(self, api, entity, prop):
        self.api = api
        self.entity = entity
        self.prop = prop

    def onactivate(self, entity, prop):
        filters = prop.Attributes.GetValue("filters", None)
        title = prop.Attributes.GetValue("title", "Save...")
        if filters is None:
            filters = "All files (*.*)|*.*"
        filPath = prop.Value
        if filPath is None:
            filPath = ""
        fileDir = os.path.dirname(filPath)
        fileName = os.path.basename(filPath)
        ret, filPath = FileDialog.ShowSaveDialog(None, fileDir, filters, 0,
            title, fileName)
        if ret == DialogResult.OK:
            prop.Value = filPath
            prop.Validate()

    def onshow(self, entity, prop):
        propsComp = entity.UserInterface.GetComponent("Properties")
        propWebObj = PropsHelper.GetPropWebObjWithName(propsComp, prop.Name)
        buttonLabel = prop.Attributes.GetValue("buttonLabel", "Edit")
        propWebObj.Buttons[0] = buttonLabel
        # 为属性按钮控件添加`ButtonClicked`点击事件
        propWebObj.ButtonClicked = CallbackWebObject("ButtonClicked", 
                                                     propsComp.Container)
        propWebObj.ButtonClicked.Tag = prop
        
        def onButtonClicked(sender, args):
            prop.Activate()
            propsComp.UpdateData()
            propsComp.Refresh()
        
        # 为属性按钮控件的`ButtonClicked`事件绑定`onButtonClicked`处理器
        propWebObj.ButtonClicked.Called += onButtonClicked

# <onactivate>回调函数
def onFileSaveActivate(step, prop):
    filters = prop.Attributes.GetValue("filters", None)
    title = prop.Attributes.GetValue("title", "Save...")
    if filters is None:
        filters = "All files (*.*)|*.*"
    filPath = prop.Value
    if filPath is None:
        filPath = ""
    fileDir = os.path.dirname(filPath)
    fileName = os.path.basename(filPath)
    ret, filPath = FileDialog.ShowSaveDialog(None, fileDir, filters, 0,
        title, fileName)
    if ret == DialogResult.OK:
        prop.Value = filPath
        prop.Validate()

# <onshow>回调函数
def onFileSaveShow(step, prop):
    propsComp = step.UserInterface.GetComponent("Properties")
    propWebObj = PropsHelper.GetPropWebObjWithName(propsComp, prop.Name)
    buttonLabel = prop.Attributes.GetValue("buttonLabel", "Edit")
    propWebObj.Buttons[0] = buttonLabel
    propWebObj.ButtonClicked = CallbackWebObject("ButtonClicked", 
                                                 propsComp.Container)
    propWebObj.ButtonClicked.Tag = prop
    
    def onButtonClicked(sender, args):
        prop.Activate()
        propsComp.UpdateData()
        propsComp.Refresh()
    
    propWebObj.ButtonClicked.Called += onButtonClicked


class PropsHelper:

    @staticmethod
    def GetPropWebObjWithName(propsComp, propName):
        stack = []
        stack.append(propsComp.GetData[PropertiesWebObject]().RootProperty)
        while stack:
            for propWebObj in stack.pop().Properties:
                if propWebObj.RefSimProperty.Name == propName:
                    return propWebObj
                if propWebObj.Properties:
                    stack.append(propWebObj)


class UserPropObj:

    def __init__(self, api, entity, prop):
        """Constructor of `UserPropObj` class
        :param api: Ansys.ACT.Interfaces.Common.IExtAPI, ExtAPI
        :param entity: Ansys.ACT.Interfaces.UserObject.IUserObject
        :param prop: Ansys.ACT.Interfaces.UserObject.ISimProperty
        """
        self.api = api
        self.entity = entity
        self.prop = prop

    def onactivate(self, entity, prop):
        """Callback that is invoked when the property is ``activated``. 
        :param entity: Ansys.ACT.Interfaces.UserObject.IUserObject, the entity 
            containing the property.
        :param prop: Ansys.ACT.Interfaces.UserObject.ISimProperty, 
            the activated property.
        """
        pass

    def value2string(self, entity, prop, value):
        """Callback that is invoked to convert the 
            value stored by the property into a string.
        :param value: object, the property value.
        :return: str, the String value.
        """
        pass

    def string2value(self, entity, prop, strVal):
        """Callback that is invoked to convert the value stored 
            by the property into a string.
        :param strVal: str, the String value.
        :return: object, the value.
        """
        pass

    def getvalue(self, entity, prop, value):
        """Callback that is invoked when the property value is acquired.
        :param value: object, the stored property value.
        :return: object, The value.
        """
        pass

    def setvalue(self, entity, prop, value):
        """Callback that is invoked  when the property value is set. 
        :param value: object, the submited value.
        :return: object, the transformed value.
        """
        pass

    def isvalid(self, entity, prop):
        """Callback that is invoked to determine whether the 
            property is valid. 
        :return: bool, `True` if the property is valid,`False` otherwise
        """
        pass

    def isvisible(self, entity, prop):
        """Callback that is invoked to determine whether the 
            property is visible.
        :return: bool, `True` if the property is visible, `false` otherwise.
        """
        pass

    def onapply(self, entity, prop):
        """Callback that is invoked  when the property 
            `apply` button is clicked.
        """
        pass

    def oncancel(self, entity, prop):
        """Callback that is invoked  when the property 
            `Cancel` button is clicked.
        """
        pass

    def oninit(self, entity, prop):
        """Callback that is invoked when the property is initialized.
        """
        pass

    def onshow(self, entity, prop):
        """Callback that is invoked when the property is shown.
        """
        pass

    def onvalidate(self, entity, prop):
        """Callback that is invoked  when the property is validated.
        """
        pass