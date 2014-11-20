def sum(a,b):
	return a+b
def use_sum(a,b,sum_):
	return sum_(a,b)+sum(a,b)
func =use_sum
r =func(5,6,sum)
print r
#Defines function with default argument
def add(a,b=2):
 return a+b
r=add(1)
print r
r=add(1,5)
print r