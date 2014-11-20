#coding=utf-8

import time
import android

droid = android.Android()

nowPage = droid.dialogGetInput(u'现在是第几页？',None)
timeStep = droid.dialogGetInput(u'请输入时间步长', u'以分为单位，可以有小数', None)

iniPage=nowPage=int(str(nowPage.result))
timeStep=float(str(timeStep.result))*60

iniTime=time.time()
 
droid.dialogCreateAlert(u'请去看书，翻页点击确定。',None)
droid.dialogSetPositiveButtonText('Yes')
droid.dialogSetNegativeButtonText('No')
droid.dialogShow()
result=droid.dialogGetResponse()
droid.setScreenBrightness(0)

if result.result["which"] == "positive":
  while True:
    nowTime=time.time()
    nowPage+=1

    if ((nowPage-iniPage)*timeStep>(nowTime-iniTime)):
      str=u'恭喜上次翻页超过进度%d秒，翻页请点击确定。'%((nowPage-iniPage)*timeStep-(nowTime-iniTime))
    else:
      str=u'哎呀上次翻页慢于进度%d秒，翻页请点击确定。'%(-(nowPage-iniPage)*timeStep+(nowTime-iniTime))
    
    droid.dialogCreateAlert(str, u'现在是第%d页'%nowPage)
    droid.dialogSetPositiveButtonText('Yes')
    droid.dialogSetNegativeButtonText('No')
    droid.dialogShow()
    result=droid.dialogGetResponse()
    droid.vibrate(100)
    if result.result["which"]!="positive":
      break
    elif (nowTime-iniTime)>45*60:
      droid.vibrate(1000)
      break
