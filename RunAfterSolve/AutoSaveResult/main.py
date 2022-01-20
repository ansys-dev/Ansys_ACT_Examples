# encoding: utf-8
import wbjn
import os

def AutoExportResults(analysis):
    # Get Workbench project `user_files` directory 
    workDir = analysis.WorkingDir
    userDir = "\\".join(workDir.split('\\')[:-4]) + "\\user_files"
    # Get Current Design Point Name
    dpCmd = "returnValue(Parameters.GetCurrentDesignPoint().Name)"
    curDp = wbjn.ExecuteCommand(ExtAPI, dpCmd)
    ExtAPI.Log.WriteMessage("Current Design Point: DP%s" % curDp)    
    resObjs = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result)
    for resObj in resObjs:
        resExportName = "DP%s_" % curDp + resObj.Name + ".png"    
        filePath = os.path.join(userDir, resExportName)
        ExtAPI.Log.WriteMessage("Export %s to %s" % (resObj.Name, filePath))
        ExportImage(resObj, filePath)
               
def ExportImage(resObj, filePath):
    resObj.Activate()
    exportJs = r'''var gr = DS.Graphics;
    gr.MemStreamWidth = 1280;
    gr.MemStreamHeight = 768; 
    gr.StreamMode = 1; // 0=normal, 1=mem
    gr.Draw2(DS.Tree.FirstActiveObjectID);
    DS.Script.doNoWireFrameResultView();
    var imgCapCtrl = gr.ImageCaptureControl;    
    imgCapCtrl.Write(0, "{0}"); // ".png":0,".jpg":1
    //So the geometry view will become visible again
    gr.StreamMode = 0;
    gr.Redraw(1)'''
    jsEngine = ExtAPI.Application.ScriptByName("jscript")
    filePath = filePath.replace("\\", "\\\\")
    jsEngine.ExecuteCommand(exportJs.format(filePath))