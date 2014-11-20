class Base:
 def __init__(self):
 	self.data =[]
 def add(self, x):
 	return self.data.append(x)
 def addtwice(self, x):
  self.add(x)
  self.add(x)
  return self.data
# Child extends Base
class Child(Base):
 def plus(self,a,b):
  self.addtwice("ss").append(str(a+b))
  return self.data

oChild =Child()
oChild.add("str1")
print oChild.data
print oChild.plus(2,3)