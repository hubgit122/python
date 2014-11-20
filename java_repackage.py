#encoding="utf-8"
import os
import json
import copy
import re
import shutil

projectDir = os.getcwd()
config =  {"platform" : "Android", "process" : [r".*\.java"], "defined": {"JAVA": "",}, "extract" : {"Android" : [r"src\\.*", r"libs\\.*", r"assets\\.*", r"jni\\.*", r"res\\.*", r"gen\\.*",  r"\.classpath", r"\.project", r"androidManifest\.xml", r"proguard\.cfg", r"project\.properties"],}, "exclude": {"Android" : [r"libs\\sqlite-jdbc.*"],}, "lineCommentBeginString" : {"java" :  "//",},}
platform = ""
process=[] #������ʽ��ʾ�����·���б�, ��ʾ��Ҫ�������define��platform��Ԥ����
predefined= {} #define���ļ�-ֵ, ��Դ��config.repackage��process�б��е��ļ�. ÿ���ļ��������, �ָ���config��״̬
defined = {}
extract=[] #��ǰƽ̨��Ҫ����ȡ���ļ������·����������ʽ
exclude = [] #��ǰƽ̨��Ҫ���ų����ļ������·����������ʽ, ʵ����ȡ����{extract}-{exclude}

#process�ļ�ע�͸�ʽ��
# "//#if[n]def xx" �� "//#platform xx" ����β��ע�����Ƶ���
# "//##if[n]def xx" �� "//##platform xx"�ڳ��˿հ��ַ�������ױ�ע�����ƴ��к������ƥ���"//##endif"��"//##endplatform"֮�����

def readConfig():
  global config
  global platform
  global predefined
  global defined
  global process
  global extract
  global exclude
  try:
    if os.path.exists("config.repackage") and os.path.isfile("config.repackage"):
      h = open("config.repackage", "r")
  except:
    return False
  config = json.load(h)
  h.close()
  platform = config["platform"]
  predefined = config["defined"]
  defined = copy.copy(predefined)

  process = iniFileList(config["process"])
  extract = iniFileList(config["extract"])
  exclude = iniFileList(config["exclude"])
  return True

def iniFileList(list):
  l = []
  for i in list:
    i = expandFileName(i)
    i = toReg(i)
    l.append(i)
  return l

def toReg(i):
  return re.compile(i)

def iniConfigFile():
  h = open("config.repackage", "w")
  json.dump(config, h)
  h.close()

def expandFileName(name):
  name = projectDir+ "\\" + name
  return trimFileName(name)

def trimFileName(file):
  file.lower()
  file.replace("/", "\\", 999)
  return file

def work(root, exroot):
  root = trimFileName(root)
  exroot = trimFileName(exroot)
  print root, exroot
  for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
      filename = dirpath + "\\" + filename
      for m in process:
        if m.match(filename):
          str = process(filename)
          h = open(filename.replace(root, exroot), "w")
          h.write(str)
          h.close()
      for ex in extract:
        if ex.match(filename):
          excluded = False
          for exc in exclude:
            if exc.match(filename):
              excluded = True
              break
          if not excluded:
            shutil.copyfile(filename, filename.replace(root, exroot))
          break

if __name__ == "__main__":
  if not readConfig():
    iniConfigFile()
  else:
    work(os.getcwd(), "d:\\")
  print "done"