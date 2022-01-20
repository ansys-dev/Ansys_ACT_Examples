# encoding: utf-8
import clr
# 引用WinForms类库
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
# 导入WinForms命名空间
from System.Windows.Forms import *
import System.Drawing
from System.Collections.Generic import List
import os
import sys

# 构建结果导出窗体界面
class ExtFrmExport(Form):

    def __init__(self):
        super(ExtFrmExport, self).__init__()
        self.Text = "Export Result"
        self.InitComponet()
        self.initListView()
        self.FrmEventHandler()
   
    # 初始化ListView控件，同步后处对象显示
    def initListView(self):
        resultList = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result)
        for result in resultList:
            listItem = ListViewItem()
            listItem.SubItems.Add(result.Name)
            self.listViewResult.Items.Add(listItem)
    
    # 窗体事件处理函数    
    def FrmEventHandler(self):
        self.btnSelect.Click += self.btnSelect_clicked
        self.btnSelAll.Click += self.btnSelAll_clicked
        self.btnSelNone.Click += self.btnSelNone_clicked
        self.btnExport.Click += self.btnExport_clicked
    
    # <文件选择...>按钮点击后执行事件函数
    def btnSelect_clicked(self, sender, e):
        exportDlg = FolderBrowserDialog()
        exportDlg.Description = "请选择结果输出的文件夹"
        exportResult = exportDlg.ShowDialog()
        if exportResult == DialogResult.OK:
            exportDir = exportDlg.SelectedPath
            self.txtReslutDir.Text = exportDir
    
    # <一键输出后处理云图>按钮点击后执行事件函数    
    def btnExport_clicked(self, sender, e):
        exportObjList = List[Ansys.ACT.Automation.Mechanical.DataModelObject]()
        for item in self.listViewResult.CheckedItems:
            exportObjList.Add(self.GetResultObjByName(item.SubItems[1].Text))            
        if self.txtReslutDir.Text:
            for res in exportObjList:
                res.Activate()			
                Graphics.ExportImage(os.path.join(self.txtReslutDir.Text, res.Name + ".png"))
        MessageBox.Show(self, "结果云图已输出完成！", "Mechanical")
                                				
    # <全选>按钮点击后执行事件函数
    def btnSelAll_clicked(self, sender, e):
        for item in self.listViewResult.Items:
            item.Checked = True
    
    # <全不选>按钮点击后执行事件函数
    def btnSelNone_clicked(self, sender, e):
        for item in self.listViewResult.Items:
            item.Checked = False      
  
    @staticmethod
    def GetResultObjByName(res_name):
        for res in ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result):
            if res.Name == res_name: return res           			 
    
    def InitComponet(self):
        self.Size = System.Drawing.Size(520, 500)
        # font
        self.Font = System.Drawing.Font("微软雅黑", 10.5, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point)
        # lblResult
        self.lblResult = Label(Text="结果文件夹：")
        self.lblResult.Size = System.Drawing.Size(100, 30)
        self.lblResult.Location=System.Drawing.Point(20, 30)
        self.lblResult.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        # txtResltDir
        self.txtReslutDir = TextBox()
        self.txtReslutDir.Size = System.Drawing.Size(280, 30)
        self.txtReslutDir.Location = System.Drawing.Point(130, 30)
        self.txtReslutDir.ReadOnly = True
        # btnSelect
        self.btnSelect = Button(Text="......")
        self.btnSelect.Size = System.Drawing.Size(50, 30)
        self.btnSelect.Location = System.Drawing.Point(425,30)
        # lblSelTip
        self.lblSelTip = Label(Text="请在表格勾选需要输出的结果")
        self.lblSelTip.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self.lblSelTip.Location = System.Drawing.Point(20, 80)
        self.lblSelTip.Size = System.Drawing.Size(220,30)
        # btnSelAll
        self.btnSelAll = Button(Text="全选")
        self.btnSelAll.FlatStyle = FlatStyle.Popup
        self.btnSelAll.Location = System.Drawing.Point(320, 80)
        self.btnSelAll.Size = System.Drawing.Size(60,30)
        # btnSelNone
        self.btnSelNone = Button(Text="全不选")
        self.btnSelNone.FlatStyle = FlatStyle.Popup
        self.btnSelNone.Location = System.Drawing.Point(400, 80)
        self.btnSelNone.Size = System.Drawing.Size(80,30)
        # listViewResult
        self.listViewResult = ListView()
        self.listViewResult.BorderStyle = BorderStyle.FixedSingle
        self.listViewResult.Location = System.Drawing.Point(20,120)
        self.listViewResult.Size = System.Drawing.Size(460,260)
        self.listViewResult.CheckBoxes = True
        self.listViewResult.View = View.Details
        self.colHeaderOne = ColumnHeader(Text="是否输出")
        self.colHeaderOne.Width = 70
        self.listViewResult.Columns.Add(self.colHeaderOne)
        self.colHeaderTwo = ColumnHeader(Text="后处理对象名称")
        self.listViewResult.Columns.Add(self.colHeaderTwo)
        self.colHeaderTwo.Width = self.listViewResult.Width - self.colHeaderOne.Width
        self.colHeaderTwo.TextAlign = HorizontalAlignment.Center
        # btnExport
        self.btnExport = Button()
        self.btnExport.Location = System.Drawing.Point(160,400)
        self.btnExport.Size = System.Drawing.Size(200,40)
        self.btnExport.Text = "一键输出后处理云图"
        # Add Controls
        self.Controls.Add(self.lblResult)
        self.Controls.Add(self.txtReslutDir)
        self.Controls.Add(self.btnSelect)
        self.Controls.Add(self.lblSelTip)
        self.Controls.Add(self.btnSelAll)
        self.Controls.Add(self.btnSelNone)
        self.Controls.Add(self.listViewResult)
        self.Controls.Add(self.btnExport)
        # Form Property
        self.TopMost = True
        self.StartPosition = FormStartPosition.CenterScreen
        self.MaximizeBox = False
        self.MinimizeBox = False

# <Export Result>按钮点击后执行事件函数
def exportRes_clicked(args):
    # args: Ansys.ACT.Automation.Mechanical.Analysis    
    frm = ExtFrmExport()
    Application.Run(frm)

# <About>按钮点击后执行事件函数
def aboutMe_clicked(args):
    MessageBox.Show("Mechanical自定义工具演示\n\nCopyright © ANSYS仿真与开发", 
        "About Me", MessageBoxButtons.OK, MessageBoxIcon.Information)        