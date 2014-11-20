class a:
	int attr
	def __new__(cls,*arg):
  	attr=3
  	print "a==cls",a==cls
  	print "dir(cls)",dir(cls)
		print "a.new"
		print "cls",cls
   return type(cls,arg,{})

class b(a):
	def __new__(cls,*arg):
		print b
	 	#print "b.__metaclass__"
		print dir(b)
		print super(a)
		return super()
		