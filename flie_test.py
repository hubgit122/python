spath="/mnt/sdcard/sl4a/scripts/baa.txt"
f=open(spath,"w") # Opens file forwriting.Creates thisfile doesn't exist.
f.write("First line 1.\n")
f.writelines(["First line 2.","ss"])
f.close()
f=open(spath,"r") # Opens file forreading
for line in f:
 print line[:-1]
 #print line[-1]
f.close()