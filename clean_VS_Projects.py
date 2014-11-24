import os

def clean(fromPath): 
    print "cleaning in", fromPath
    for root, dirs, files in os.walk(fromPath) : 
        for file in files:
            if "." in file and file.split(".")[-1] in ["sdf", "pch", "ipch", "res", "tlog", "obj", "pdb", "idb"]:
                os.remove(os.path.join(root, file))
                            
if __name__=='__main__': 
    fromPath =  raw_input("path: ")
    if len(fromPath) == 0:
        fromPath = os.getcwd()
    clean(fromPath)     
    print "done!"
    