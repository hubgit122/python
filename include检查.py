#coding=utf-8
import string, os, sys, copy

if __name__ == '__main__':
    print "toolet to examine if there are include-loop, information is in English, but errors in Chinese, enjoy------"
    roots = "E:\\Projects\\android\\gamest\\jni\\core" #raw_input("--------------input project root dirs, use comma to separate. \n")

    def getFileName(i):
        return i.split("\\")[-1]

    roots = roots.split(",")

    files = []
    for dir in roots:
        for root, dirs, files_ in os.walk(dir):
            for name in files_:
                files.append(os.path.join(root, name))

    print "-------------- *.h* files detected: "

    # 加入一个字典, 字典的首项是头文件的文件名, 尾项是头文件中包含的文件.
    reliability = {}

    fileCount = 0
    while fileCount < len(files):
        fileName = files[fileCount]
        relied = []
        if fileName.find(".h") <> -1:
            if os.path.exists(fileName):
                fileHandle = open (fileName)
                print fileName
            else:
                print fileName, "未能找到, 请检查给定文件夹是否出错, 或者是否对标准库的头文件用了""包围, 后面的分析会继续包括此文件, 但若此文件不是标准库文件, 则它的成环分析将丢失. "
                del files[fileCount]
                continue

            fileCount += 1
            if fileCount > 1000:
                print "-------------文件过多, 为了安全, 停止加入文件而继续分析. 可以修改代码来提高上限. "
                break

            dirOfThisFile = fileName.replace("/","\\")
            dirOfThisFile = dirOfThisFile.split("\\")
            dirOfThisFile = dirOfThisFile[:-1]

            for line in fileHandle.readlines():
                if line.startswith("#include"):
                    line = line.replace("/","\\")
                    if line.find("\"") <> -1:
                        included = line.split("\"")[1]

                        if included.find(":") == -1:       #路径有盘符, 表示是绝对路径
                            nowDir = copy.deepcopy(dirOfThisFile)

                            for temp in included.split("\\"):
                                if temp == "..":
                                    if len(nowDir) >1 :
                                        nowDir = nowDir[:-1]
                                    else:
                                        print "文件读取有误:", "\\".join(included)
                                else:
                                    nowDir.append(temp)
                            included = "\\".join(nowDir)

                        if not (included in files):
                            files.append(included)

                        if relied.__contains__(included):
                            print "-------",fileName, "里两次包含了", included, "不是致命错误, 可以检查一下"
                        else:
                            relied.append(included)
            reliability[fileName] = relied
        else:
            del files[fileCount]


    print "-----------detected reliablities: "
    inverseAdjacency = {}
    for item in reliability.items():
        if not inverseAdjacency.has_key(item[0]):
            inverseAdjacency[item[0]] = []
        print getFileName(item[0]),"=>",
        for i in item[1]:
            print getFileName(i),
        print
        for relied in item[1]:
            if inverseAdjacency.has_key(relied):
                inverseAdjacency[relied].append(item[0])
            else:
                inverseAdjacency[relied] = [item[0]]

    print "-----------checking if can fit TopologicalSort"
    print "--------------inverse adjacency: "
    for item in inverseAdjacency.items():
        print getFileName(item[0]),"<=",
        for i in item[1]:
            print getFileName(i),
        print

    print "---------------TopologicalSort"
    while len(inverseAdjacency)>0:
        toBeCleared = []
        for item in inverseAdjacency.items():
            if len(item[1])==0:
                toBeCleared.append(item[0])

        if len(toBeCleared)==0 and len(inverseAdjacency)>0:
            print "**********出现循环包含:"
            for item in inverseAdjacency.items():
                print getFileName(item[0]), "<=",

                for i in item[1]:
                    print getFileName(i),
                print
            break

        print "to be cleared in this loop:"
        for item_ in toBeCleared:
            print item_
            del inverseAdjacency[item_]
            for item in inverseAdjacency.items():
                if item[1].__contains__(item_):
                    item[1].__delitem__(item[1].index(item_))

    print "-----------exiting"
    print "Sum of *.h* files analyzed: ", fileCount, len(files)
