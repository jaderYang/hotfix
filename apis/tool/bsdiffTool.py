import bsdiff4
import os
import hashlib

class BsdiffTool(object):

    def getPatch(self,path1,path2,patchPath):
        bsdiff4.file_diff(path1, path2, patchPath)
        dirname = os.path.dirname(path1)
        newFilePath = os.path.join(dirname, 'newFilePath.txt')
        bsdiff4.file_patch(path1, newFilePath, patchPath)

        return 'patch creat success'

    def getFileMd5(self, filePath):
        if not os.path.isfile(filePath):
            return
        myHash = hashlib.md5()
        f = open(filePath, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myHash.update(b)
        f.close()
        return myHash.hexdigest()
