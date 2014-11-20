class Person:
 def __init__(self, name):
  self.sayHi = name 
 def sayHi(self):
  print 'Hello, my name is'

p = Person('Swaroop')
#p.sayHi()
#Person('Swaroop').sayHi()
print p
print str(p)

#print str(Person('Swaroop').sayHi())

#print str(Person.sayHi)
#print str(Person.sayHi())
print Person.__new__