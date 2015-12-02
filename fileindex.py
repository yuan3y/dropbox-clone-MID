import os.path
import filemeta
import json
from server.server import walkFiles

def getIndex(index,dir="./"):
    meta_data_dict = dict()
    listFiles=[]
    listFolders=[]
    walkFiles(listFiles,listFolders,dir)
    for filename in listFiles:
        meta_data_dict.setdefault(filename,filemeta.filemeta(filename))
    index={'listfiles': meta_data_dict, 'listfolders': listFolders}
    print(index)

# index=[]
# getIndex(index,dir="./server/store/")