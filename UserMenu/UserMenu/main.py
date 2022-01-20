# encoding: utf-8
import System
import clr
from System.Collections.Generic import List

clr.AddReference("Ans.UI")
from Ansys.UI import UIManager, MenuEntityType
from Ansys.UI.Interfaces import IGuiOperation

clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
from Ansys.UI.Toolkit import *

# 获取UIManager对象实例，管理用户界面
uiMgr = UIManager.Instance
window = Window.ActiveWindow

# 创建自定义菜单
def CreateMenu(context):
    menuMgr = uiMgr.MenuManager
    imgLib = Ansys.UI.Toolkit.ImageLibrary()
    for imgDir in ExtAPI.Extension.GetImageDirectories():
        imgLib.AddImagesFromDirectory(imgDir)
    menuLoc = List[System.String]()
    menuLoc.Add("Custom Menu")
    menuMgr.AddDynamicEntity(MenuEntityType.MenuEntry, 
        "About", "about", imgLib, 1.0, menuLoc, AboutMeOperation())

# 移除自定义菜单
def RemoveMenu(context):
    menuMgr = uiMgr.MenuManager 
    menuMgr.RemoveDynamicEntity("DynamicEntity:Menu:System.Collections.Generic.List`1[System.String]:About")     

# 继承IGuiOperation接口类，实现接口方法
class AboutMeOperation(IGuiOperation):
    # 定义菜单点击后执行的事件方法
    def Invoke(self, context):
        MessageBox.Show(window,"Workbench自定义菜单演示\n\nCopyright © ANSYS仿真与开发",
            "About Me", MessageBoxType.Info, MessageBoxButtons.OK)
    
    # 控制菜单控件显示
    def GuiItemCallBack(self, context):
        context.Visible = True
        context.Enabled = True

