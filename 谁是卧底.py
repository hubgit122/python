#coding=utf-8
import android
import time
import random
droid=android.Android()

while True:
  droid.dialogGetInput(u'重新开局，点击确定。',None)
  s1=droid.dialogGetInput(u'输入第一个词语，点击继续',None).result
  s2=droid.dialogGetInput(u'输入第二个词语，点击继续',None).result
  if s1==None or s2==None:
    break
  
  spy=random.randint(1,4)
  for i in range(1,5):
    droid.dialogGetInput(u'点击确定查看你的词',None)
    if spy==i:
      str=u'你的词是'+s1+u'，点击确定，并传递给下一个人'
    else:
      str=u'你的词是'+s2+u'，点击确定，并传递给下一个人'
    droid.dialogGetInput(str,None)
    