i=int(raw_input("begin number"))
s=int(raw_input("step"))
while raw_input("another 50?")=="":
 k=0
 while k<50:
  if str(s) in str(i) or i%s==0:
  	print "**",i,"**"
  else:
   print i
   k=k+1
  i=i+1
