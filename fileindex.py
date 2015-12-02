import os.path
import filemeta


def walkFiles(listFiles, listFolders, dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            listFiles.append(path)
        if os.path.isdir(path):
            listFolders.append(path)
            walkFiles(listFiles, listFolders, path)


def getIndex(dir="./"):
    meta_data_dict = dict()
    listFiles = []
    listFolders = []
    walkFiles(listFiles, listFolders, dir)
    for filename in listFiles:
        meta_data_dict.setdefault(filename, filemeta.filemeta(filename))
    index = {'listfiles': meta_data_dict, 'listfolders': listFolders}
    return index
