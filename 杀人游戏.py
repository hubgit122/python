#coding=utf-8
import android
import time
import random
droid=android.Android()

while True:
  droid.dialogCreateAlert(u'重新开局？点击继续……')
  droid.dialogSetPositiveButtonText('Yes')
  droid.dialogSetNegativeButtonText('No')
  droid.dialogShow()
  result = droid.dialogGetResponse()
  if result.result["which"]!="positive":
    break
  killer=random.randint(1,4)
  for i in range(1,5):
    droid.dialogCreateAlert(u'点击确定查看你的身份')
    droid.dialogSetPositiveButtonText('Yes')
    droid.dialogSetNegativeButtonText('No')
    droid.dialogShow()
    droid.dialogGetResponse()
    
    if killer==i:
      str=u'你是杀手，点击确定，并传递给下一个人'
    else:
      str=u'你是平民，点击确定，并传递给下一个人'
    droid.dialogCreateAlert(str,u"如果你不是第%d个人，或者接手时看到的就是这个界面，说明前方有人搞错了。"%i)
    droid.dialogSetPositiveButtonText('Yes')
    droid.dialogSetNegativeButtonText('No')
    droid.dialogShow()
    droid.dialogGetResponse()
 