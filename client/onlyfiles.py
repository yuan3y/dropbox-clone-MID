from os import walk

files = []
folders = []
for (dirpath, dirnames, filenames) in walk("./store/"):
    folders.append(dirpath)
    files.extend(dirpath + v for v in filenames)

print(files)
print(folders)