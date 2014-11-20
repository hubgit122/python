#encoding=utf-8
import copy

def acc(cnt,lap=1,wid=9):
	cnt[-lap]+=1
	for i in range(wid):
		if cnt[-i-1]>i:
			cnt[-i-1]-=i+1			#假设参数cnt已经符合要求
			if i!=wid-1:
				cnt[-i-2]+=1
			else:
				return True
	else:
		return False					#返回是否已遍历结束

def notNearIfAvrNotBefore(arr,i,j,lap=1):
	"""如果i, j的平均数不在i, j之前, 就不允许ij直接相邻"""
	try:
		ii = arr.index(i)
		ij = arr.index(j)
		if ((ii - ij) ** 2 == 1):
			try:
				ia = arr.index((i+j)//2) 
				return ia< ii and ia <ij
			except:
				return False
		else:
			return True
	except:
		return True

def check(arr):
	ok=True
	ok&=notNearIfAvrNotBefore(arr,1,3)
	ok&=notNearIfAvrNotBefore(arr,1,7) 
	ok&=notNearIfAvrNotBefore(arr,1,9) 
	ok&=notNearIfAvrNotBefore(arr,3,7) 
	ok&=notNearIfAvrNotBefore(arr,3,9) 
	ok&=notNearIfAvrNotBefore(arr,7,9) 
	ok&=notNearIfAvrNotBefore(arr,2,8) 
	ok&=notNearIfAvrNotBefore(arr,4,6)
	return ok

def fac(x):
	if x<=1:
		return 1;
	return x*fac(x-1)
 
if __name__=="__main__":
	array=[]
	count=[]
	modelnum=0
	for i in range(9):			#int(raw_input("几元排列？"))):
		array.append(i+1)
		count.append(0)

	lap = 0
	while lap != 6:
		finish = False
		lap +=1 
		print lap 
		while not finish:
			array_=[]
			temp=copy.copy(array)
			for i in range(9-lap+1):
				array_.append(temp.pop(count[i]))
			modelnum += check(array_[0:9-lap])
			finish=acc(count,lap)
	print modelnum