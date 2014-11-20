#coding=utf-8
def F(x):
	"""ssq fac"""
	if x<=1:
		return 1;
	return x*(F(x-1)+1)

def f(x):
	"""normal fac"""
	if x<=1:
		return 1;
	return x*f(x-1)

def A(n,m):
	return f(n)/f(n-m)

if __name__=="__main__":
	temp=0
	for i in range(9,3,-1):
		temp+=A(9,i)
	print temp

