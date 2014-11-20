#coding=utf-8
import android
import time
droid=android.Android()

while True:
  droid.makeToast("去学习！")
  time.sleep(60*45)
  droid.vibrate("1000")
  droid.makeToast("休息！")
  droid.vibrate("1000")
  time.sleep(3*45)