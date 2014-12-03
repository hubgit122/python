#coding=utf-8
import os
import sys
import json
import copy
import re
import shutil

projectDir = os.getcwd()
config =  {
    "defined": {},
    "deleteComment": {
        "c": 0,
        "classpath": 0,
        "cpp": 0,
        "h": 0,
        "java": 0,
        "project": 0,
        "xml": 0
    },
    "exclude": {
        "All": [
            "jni/core/jniCore"
        ],
        "Android": [
            "libs/sqlite-jdbc.*"
        ],
        "Java": [
            "libs/sqldroid.*"
        ]
    },
    "extract": {
        "All": [
            "src/.*",
            "libs/.*",
            "assets/.*",
            "jni/.*",
            "\\.classpath",
            "\\.project"
        ],
        "Android": [
            "res/.*",
            "gen/.*",
            "androidmanifest\\.xml",
            "proguard\\.cfg",
            "project\\.properties"
        ],
        "Java": []
    },
    "lineCommentBeginString": {
        "classpath": "<!--",
        "project": "<!--",
        "java": "//",
        "xml": "<!--",
        "c" : "//",
        "cpp": "//", 
        "h": "//",
    },
    "platform": "Android",
    "process": [
        r"src/.*\.java",
        r"\.classpath",
        r"\.project"
    ]
}

platform = ""
process=[] #正则表达式表示的相对路径列表, 表示需要进行针对define和platform的预处理
predefined= {} #define过的键-值, 来源有config.repackage和process列表中的文件. 每个文件处理完后, 恢复到config的状态
defined = {}
extract=[] #当前平台需要被提取的文件的相对路径的正则表达式
exclude = [] #当前平台需要被排除的文件的相对路径的正则表达式, 实际提取的是{extract}-{exclude}
handled = False
word = re.compile("[a-zA-Z_][a-zA-Z_0-9]*")
nonspace = re.compile(r"[^\s]+")
defWord = re.compile(r"`[a-zA-Z_][a-zA-Z_0-9]*`")

#process所含文件预处理命令注释格式： 以下用"//"代替所在文件的行注释符, 不同拓展名文件的行注释符在config里声明
# "//#define xx yy " define前面不能空格, yy后面一定要是空格或者行尾
# "//#if[n]def xx [...]" 或 "//#platform xx [...]" 在行尾标注，控制单行
# "//##if[n]def xx [...]" 或 "//##platform xx [...]" 控制下一行直到遇到与之匹配的"//##endif"或"//##endplatform"
# ... 可以是define xx yy,define xx ,define xx, 最后的逗号随意保留, define前面不能有空格 被xx和yy之间要空格, 后面随意空格
# [...]可以省略
# 也可以把块注释作为行注释使用, 这里并不严格检查
# 在行中使用``包围一个token, 将检查defined表, 用已经define的字符串替代. 可以多次使用

def readConfig():
  global config
  global platform
  global predefined
  global defined
  global process
  global extract
  global exclude

  if os.path.exists("config.repackage") and os.path.isfile("config.repackage"):
      h = open("config.repackage", "r")
  else:
    return False

  config = json.load(h)
  h.close()
  platform = config["platform"]
  predefined = config["defined"]
  predefined["platform"] = platform
  if not predefined.has_key(platform): predefined[platform] = ""
  defined = copy.deepcopy(predefined)

  process = iniFileList(config["process"])

  try:
    exclude += iniFileList(config["exclude"][platform])
  except:
    print "WANING: exclude of platform", platform, "not defined"
  try:
    extract += iniFileList(config["extract"][platform])
  except:
    print "WANING: extract of platform", platform, "not defined"
  try:
    exclude += iniFileList(config["exclude"]["All"])
  except:
    print "WANING: exclude of All not defined"
  try:
    extract += iniFileList(config["extract"]["All"])
  except:
    print "WANING: extract of All not defined"
  return True

def iniFileList(list):
  l = []
  for i in list:
    s = expandFileName(i)
    re = toReg(s)
    l.append(re)
  return l

def toReg(i):
  return re.compile(i, re.I)

def iniConfigFile():
  h = open("config.repackage", "w")
  json.dump(config, h ,sort_keys=True, indent=4)
  h.close()

def expandFileName(name):
  name = trimFileName(projectDir)+ "/" + name.lower()
  return name

def trimFileName(file):
  s = file.lower()
  s = file.replace("\\", "/")
  return s

def trimFileNames(list):
  l = []
  for i in list:
    l.append(trimFileName(i))
  return l

def processFile(fileName):
  global config
  global platform
  global predefined
  global defined
  global process
  global extract
  global exclude
  global handled

  def checkBlock(lineparts, blockValid, wd):
    global handled
    if lineparts[1].startswith(wd):
      token = word.findall(lineparts[1][len(wd) + 1:])[0]
      if wd == "platform":
        blockValid.append(token == platform)
      else:
        blockValid.append(token in defined.keys())
      handled = True
    else:
      handled = False

  def checkLine(lineparts, wd):
    global handled
    if lineparts[1].startswith(wd):
      token = word.findall(lineparts[1][len(wd) + 1:])[0]
      handled = True
      if wd == "platform":
        return token == platform
      else:
        return token in defined.keys()
    else:
      return False

  def info(lnum, fileName, inf):
    print "info in", fileName, "line", lnum, inf

  def addDef(inst, defined, lnum, fileName):
    tmp = nonspace.findall(inst)
    if len(tmp) >= 2:
      if defined.has_key(tmp[1]):
        info (lnum, fileName, "redefine: " +  tmp[1])
    try:
      defined[tmp[1]] = tmp[2]
    except:
      try:
        defined[tmp[1]] = ""
      except:
        info(lnum, fileName, "define xx yy")

  def addDefs(lineparts, defined, lnum, fileName):
    if "[" in lineparts[1] and "]" in lineparts[1]:
      instructions = lineparts[1][lineparts[1].find("[") + 1: lineparts[1].find("]")]
      for inst in instructions.split(","):
        # 处理define
        if "define" in inst:
          addDef(inst, defined, lnum, fileName)

  defined = copy.deepcopy(predefined)
  h = open(fileName, "r")
  cms = config["lineCommentBeginString"][getExt(fileName)]
  deleteComment = config["deleteComment"][getExt(fileName)]
  lines = h.readlines()
  trimedLines = []
  blockValid = []
  lnum = 0
  for line in lines:
    lnum += 1
    handled = False #表示有可用处理方案
    defValid = False #表示声明正确, 后面的define语句应该被执行

    if blockValid:
      #isTrue非空, 在控制块内
      if cms + "##end" in line:
        if blockValid[-1]:
          if deleteComment:
            trimedLines.append(line.split(cms + "##end")[0])
          else:
            trimedLines.append(line)
        blockValid.pop()
        continue  #跳过进一步处理
      elif not blockValid[-1]:
        continue

    #不论在块内块外, 行处理逻辑相同
    lineparts = line.split(cms)
    line = lineparts[0]
    defParts = line.split("`")
    if len(defParts) % 2 == 0:
      info(lnum, fileName, "define not closed")
    else:
      i = 0
      for i in range(len(defParts) / 2):
        try:
          defParts[2 * i + 1] = defined[defParts[2 * i + 1]]
        except:
          defParts[2 * i + 1] = "`" + defParts[2 * i + 1] + "`"
    line = "".join(defParts)
    lineparts[0] = line
    line = cms.join(lineparts)

    if cms + "##" in line:
      #块控制开始
      lineparts = line.split(cms + "##")
      checkBlock(lineparts, blockValid, "ifdef")
      checkBlock(lineparts, blockValid, "ifndef")
      checkBlock(lineparts, blockValid, "platform")
      defValid = blockValid[-1]
    elif cms + "#define" in line:
      lineparts = line.split(cms + "#")
      #控制单行
      addDef(lineparts[1], defined, lnum, fileName)
    elif cms + "#" in line:
      lineparts = line.split(cms + "#")
      defValid |= checkLine(lineparts, "ifdef")
      defValid |= checkLine(lineparts, "ifndef")
      defValid |= checkLine(lineparts, "platform")
    else:
      lineparts = [line]

    if handled and defValid:
      addDefs(lineparts, defined, lnum, fileName)

    if not handled or defValid:
      if deleteComment:
        trimedLines.append(lineparts[0])
      else:
        trimedLines.append(line)

  return trimedLines

def getExt(fileName):
  s = ""
  try:
    s = fileName.split(".")[-1]
  except:
    s = ""
  return s

def work(root, exroot):
  root = trimFileName(root)
  exroot = trimFileName(exroot)

  if os.path.exists(exroot):
    filenames=os.listdir(exroot)
    if filenames:
      if raw_input(exroot + " not empty! go ahead anyway?[y/n]") != "y":
        return
      else:
        for f in filenames:
          f = exroot + "/" + f
          if os.path.isfile(f):
            os.remove(f)
            print f+" removed!"
          elif os.path.isdir(f):
            shutil.rmtree(f,True)
            print "dir "+f+" removed!"

  for dirpath, dirnames, filenames in os.walk(root):
    dirpath = trimFileName(dirpath)
    for filename in filenames:
      filename = dirpath + "/" + filename
      exFile = filename.replace(root, exroot)
      exDir = dirpath.replace(root, exroot)

      processed = False
      for m in process:
        if m.match(filename):
          if not os.path.exists(exDir):
            os.makedirs(exDir)
          h = open(exFile, "w")
          h.writelines(processFile(filename))
          h.close()
          processed = True
          print "processed", filename
          break
      if processed:
        continue

      for ex in extract:
        if ex.match(filename):
          excluded = False
          for exc in exclude:
            if exc.match(filename):
              excluded = True
              break
          if not excluded:
            processed = True
            if not os.path.exists(exDir):
              os.makedirs(exDir)
            shutil.copyfile(filename, filename.replace(root, exroot))
            print "extract", filename
          break
      if not processed:
        print "file", filename, "ignored"

if __name__ == "__main__":
  default_encoding = 'utf-8'
  if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)  
  if not readConfig():
    iniConfigFile()
    print "请编辑本目录下的config.repackage文件, 作为配置, 并再次运行本脚本"
  else:
    work(os.getcwd(), os.getcwd() + "/ports/" + config["platform"])
  print "done"