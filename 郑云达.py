#coding=utf-8

import time
import android

droid = android.Android()

timeStep = droid.dialogGetInput(u'请输入时间步长', u'以分为单位，可以有小数', None)

timeStep=float(str(timeStep.result))*60

i=1
while True:
	time.sleep(timeStep)
	droid.vibrate(300)
	i+=1
	droid.notify('title', 'message')
	droid.makeToast(u'第%d次时间到，是第%.2f分'%(i, i*timeStep/60) )
	#droid.ttsSpeak( u'时间到，%.2f分'%(i*timeStep/60) )
	