#coding=utf-8
import android
droid=android.Android()
str=droid.dialogGetInput(u'请去看书，翻页点击确定。',None).result
str.decode("base64")