# encoding: utf-8

# 数字输入：值范围[10.0, 1000)
def IsNumInputValid(step, prop):
    if 10 <= prop.Value < 1000:        
        return True
    return False

# 字符输入：字母、数字和下划线，长度大于6
# 使用正则表达式："[a-zA-z0-9_]{6,}$"    
def IsTextInputValid(step, prop):
    import re
    if prop.Value and re.match("[a-zA-z0-9_]{6,}$", prop.Value):
        return True
    return False


def onInputStepUpdate(step):
    pass