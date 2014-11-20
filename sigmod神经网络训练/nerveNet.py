#coding=utf-8 
#!/usr/bin/env python 
#Filename: nerveNet.py

import  os
import copy
import math
from random import random,randint
from utilities import * 

#----------------------------------------------------------------------
class Vector(list):
	"""向量类, 实现了方法: 点乘, 数乘, 归一化"""
	#----------------------------------------------------------------------
	def __init__(self, iniList=None, iniDiscription=None, ss=[]):
		"""向量存储初始化, 给内部存储赋值, iniList可以作为参数"""
		if iniList == None or iniList == []:
			r= getPositiveInt("Input rows of Vector, %s:"%(iniDescription))
			for i in range(0,r):
				self.append(float(raw_input("input V[%d]" % i )))
		else:
			for i in range(0, len(iniList)):
				self.append(float(iniList[i]))

	#----------------------------------------------------------------------
	def dot(self, V_):
		"""向量点乘"""
		assert len(V_) == len(self)
		if len(V_) == len(self):
			temp = 0;
			for i in range(0, len(V_)):
				temp += V_[i] * self[i];
			return temp
		else:
			return None
	#----------------------------------------------------------------------
	def norm(self):
		"""取模长"""
		return math.sqrt(self.dot(self))

	#----------------------------------------------------------------------
	def stretch(self, c):
		"""向量数乘"""
		for i in range(len(self)):
			self[i] *= c
	#----------------------------------------------------------------------
	def normalize(self):
		"""向量归一化"""
		temp = self.norm()
		if temp <= 10 ** -6:
			pass
		else:
			self.stretch(1/temp)

#----------------------------------------------------------------------
class TLU(Vector):
	"""threshold logic unit, 阈值逻辑单元, 实现了方法: 初始化, 求输出, 求sigmod函数, 训练"""
	#----------------------------------------------------------------------
	def __init__(self, TLU_description="", inNum=None, W_=[]):
		"""初始化, 下划线后缀代表向量"""
		if inNum == None or inNum <= 0 or type(inNum) != int:
			inNum = getPositiveInt("How many inputs of TLU %s? "%(TLU_description))
		inNum += 1				#下边使用扩展权值
		if len(W_) != inNum:
			if  'y' in raw_input("So, you wanna use random weightVector?(y/n)"):
				for i in range(0, inNum):
					self.append(float(random()))
			else:
				for i in range(0, inNum):
					self.append(getFloat(raw_input("Input W[%d] of TLU%s"%(i,TLU_description))))
		else:
			for i in range(0, len(W_)):
				self.append(float(W_[i]))
		self.normalize();
		print TLU_description, "weightVector\n",self

	#----------------------------------------------------------------------
	def s(self, x):
		"""得到W与X的点积, x是扩展的输入变量, 最后的分量1不用输入"""
		if len(x) != len(self) - 1:
			return None
		else:
			temp=0
			for i in range(0,len(x)):
				temp += self[i] * x[i]
			temp += self[-1]
			return temp;

	#----------------------------------------------------------------------
	def f(self, x):
		"""得到sigmod函数, x是扩展的输入变量, 最后的分量1不用输入"""
		if self.s(x)>1000.0:
			result = 0
		elif self.s(x)<-1000.0:
			result = 1
		else:
			result = 1 / (1 + math.exp( - s(x) ) )
		return result

	#----------------------------------------------------------------------
	def out(self, x):
		"""得到真实的输出, x是扩展的输入变量, 最后的分量1不用输入"""
		if self.s(x) > 0:
			return 1
		else:
			return 0

	#----------------------------------------------------------------------
	def train(self,XY):
		"""训练方法, XY是训练向量, x为省略分量1的扩展输入向量, y为期望的输出"""
		learnCoefficient= 0.01
		out= self.f(XY[0:-1])
		for i in range(0,len(self)-1):
			self[i]=self[i]+learnCoefficient*(XY[-1]-out)*out*(1-out)*XY[i]
		self[-1]=self[-1]+learnCoefficient*(XY[-1]-out)*out*(1-out)
		self=self.normalize()


#----------------------------------------------------------------------
class nerveNet(list):
	"""神经网络, 由TLU组成, 用反向传播法训练每一个TLU. 实现方法: 初始化, 训练"""
	#----------------------------------------------------------------------
	def __init__(self, inNum=None, layerNum = None, W___ = []):
		"""分层向前初始化内部的TLU, 三下划线后缀代表三维列表"""
		try:
			os.remove("NerveNet Testing Log.txt")
		except:
			pass
		try:
			os.remove("NerveNet Trainning Log.txt")
		except:
			pass
		if inNum == None or inNum <= 0 or type(inNum) != int:
			self.inNum = getPositiveInt("How many inputs of nerveNet? ")
		else:
			self.inNum = inNum
		if layerNum == None or layerNum <= 0 or type(layerNum) != int:
			layerNum = getPositiveInt("How many layers of nerveNet? ")
			for i in range(0, layerNum):
				self .append([])
		if len(W___) != layerNum:
			if "y" in raw_input("Default W Matrix doesn't satisfy the length, use zeros weightVector? (y/n)"):
				self.__writeW(layerNum, "zero")
			elif "y" in raw_input("So, you wanna use random weightVector? (y/n)"):
				self.__writeW(layerNum, "random")
			else:
				self.__writeW(layerNum, "input")
		else:
			insOfLayer = [self.inNum]
			for i in range(0, layerNum):
				self.append([])
				TLU_Num = len(W___[i])
				insOfLayer.append(TLU_Num)
				for j in range(0, TLU_Num):
					self[i].append(TLU("[%d][%d]"%(i, j), insOfLayer[i], W___[i][j]))
		print "NerveNet weightVectors\n",self

	#----------------------------------------------------------------------
	def s(self, x=[]):
		"""得到点积形式的输出, x是扩展的输入变量, 最后的分量1不用输入"""
		if len(x) != self.inNum:
			return None
		else:
			self.lastX = [x]				#lastX是每层的输入向量, 求解输出时保存所有层
			for i in range(len(self)):
				Y = []				#输出向量, 每层更新
				for j in range(len(self[i])):
					Y.append(self[i][j].s(self.lastX[i]))
				self.lastX.append(Y)
			return Y;

	#----------------------------------------------------------------------
	def f(self, x):
		"""得到sigmod函数形式的输出, x是扩展的输入变量, 最后的分量1不用输入"""
		Y = self.s(x)
		resault = []
		for y in Y:
			if y>1000.0:
				resault.append(0)
			elif y<-1000.0:
				resault.append(1)
			else:
				resault.append(1 / (1 + math.exp( - y ) ))
		return resault

	#----------------------------------------------------------------------
	def out(self, x):
		"""得到真实的输出, x是扩展的输入变量, 最后的分量1不用输入"""
		if len(x) != self.inNum:
			return None
		else:
			self.lastX = [x]					#lastX是每层的输入向量, 求解输出时保存所有层
			for i in range(len(self)):
				Y = []					#输出向量, 每层更新		其实输入就是上次的输出, 只是借助Y暂存
				for j in range(len(self[i])):
					Y.append(self[i][j].out(self.lastX[i]))
				self.lastX.append(Y)
			return Y;

	#----------------------------------------------------------------------
	def trainOnce(self, XY):
		"""训练一次方法, 反向传播. XY是包含输入向量和结果向量的混合向量"""
		learnCoefficient = 1		
		Y= self.f(XY[0:-len(self[-1])])			#将Y分离开. 从后面去掉最后一层的个数这么多个
		delt = Vector(  [(XY[-len(self[-1])+j] - Y[j]) * Y[j] * (1 - Y[j]) for j in range(len(self[-1]))]  ) #分层计算, 每层delt的个数与对下一层的输出个数一致
		for i in range(len(self)-1, -1, -1):
			for j in range(len(self[-1])):
				for k in  range(len(self[-1][j])-1):
					self[i][j][k] += learnCoefficient * delt[j] * self.lastX[i][k]
				self[i][j][-1] += learnCoefficient * delt[j]
				self[i][j].normalize()
			if i >= 1:
				delt = self.backpropagate(delt, i-1)

	#----------------------------------------------------------------------
	def backpropagate(self, delt, i):
		"""得到由第i+1层的delt向量得到第i层的delt向量"""
		delt_ = copy.deepcopy(delt)
		delt = []
		for j in range(len(self[i])):
			temp = 0
			for l in range(len(self[i+1])):
				temp += delt_[l] * self[i+1][l][j]
			delt.append(self.lastX[i+1][j] * (1 - self.lastX[i+1][j]) * temp)
		return delt

	#----------------------------------------------------------------------
	def train(self, trainingSet):
		"""训练方法, 训练到满足输入为止, 限制10**4步, 还没有收敛, 可能现有TLU的个数和分布不能满足要求"""
		count = 0
		fout = file("NerveNet Trainning Log.txt", "a")
		while count < 10 ** 4:
			if count % 10 == 0:					#判断一次需要对所有的训练集内的向量求解一次输出, 每训练十次检查一次
				if self.test(trainingSet)== True:
					break
			ran=randint(0,len(trainingSet)-1)
			fout.write("\n#----------------------------------------\ntrainingVector\n%s"%(str(trainingSet[ran]), ))
			self.trainOnce(trainingSet[ran])
			fout.write("\nweightVector after training\n%s"%str(self))
			count += 1
		else:
			fout.write("\n#----------------------------------------\nweightVector after training\n%s"%str(self))
		fout.close()

	#----------------------------------------------------------------------
	def test(self, trainingSet):
		"""测试训练集是不是被完全满足"""
		fout = file("NerveNet Testing Log.txt", "a")
		for i in range(len(trainingSet)):
			if self.out(trainingSet[i][0:self.inNum])!=trainingSet[i][self.inNum:]:
				fout.write("%d Vector(s) Matched, but vetor %s not matched! \n"%(i, str(trainingSet[i])))
				return False
		else:
			fout.write("All Vectors Matched!\n")
			return True
		fout.close()

	#----------------------------------------------------------------------
	def __writeW(self, layerNum, des="zero"):
		"""写权重, 标记字符串区分写入方式"""
		insOfLayer = [self.inNum]
		for i in range(0, layerNum):
			TLU_Num = getPositiveInt("How many TLUs in layer %d?"%(i+1))
			insOfLayer.append(TLU_Num)
			for j in range(0, TLU_Num):
				W_ = []
				for k in range(0, insOfLayer[i]+1):
					if des == "zero":
						W_.append(float(0.0))
					elif des == "random":
						W_.append(random())
					else:
						W_.append(getFloat("W[%d] of TLU[%d][%d]"%(k, i, j)))
				self[i].append(TLU("[%d][%d]"%(i, j), insOfLayer[i], W_))



if __name__ == '__main__':
    #nn = nerveNet(3, 3, [[[random(), random(), random(), random()], [random(), random(), random(), random()]], [[random(), random(), random()], [random(), random(), random()]], [[random(), random(), random()]]])
    #trainingSet=[[1,0,0,1],[0,1,1,0],[1,1,0,1],[1,1,1,0],[0,0,1,0],[1,0,1,1]]
    #nn.train(trainingSet)
    nn = nerveNet(3, 1, [[[0.12210976361991092, -0.66897477130056937, -0.72435737306071157, -0.11343878121976438]]]) #[[[0, 0, 0, 0]]])
    trainingSet=[[1,0,0,1],[0,1,1,0],[1,1,0,1],[1,1,1,0],[0,0,1,0],[1,0,1,1]]
    nn.train(trainingSet)
