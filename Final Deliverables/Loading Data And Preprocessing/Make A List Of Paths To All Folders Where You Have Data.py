dirName = 'D:/TSB Projects/Digital Naturalist/augmented data'
folders = listdir(dirName)

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for fol name in listOfFile:
        fullPath = os.path.join(dirName,fol_name)
        allFiles.append(fullPath)
    return allFiles

Folders = getListOfFiles(dirName)
len(Folders)
subfolders = []
for num in range(len(Folders)):
    sub_fols = getListOfFiles(Folders[num])
    subfolders+=sub_fols
subfolders
