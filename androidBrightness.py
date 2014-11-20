import android
droid=android.Android()
brightness= droid.getScreenBrightness()
droid.setScreenBrightness(-100)
raw_input("")
droid.setScreenBrightness(brightness[1])