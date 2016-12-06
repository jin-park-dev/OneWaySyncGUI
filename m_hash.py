import hashlib

def openFile(file_name):
    file = open(file_name, 'rb')
    file_binary = file.read()
    file.close()
    return file_binary

def calcHash(file_binary):
    file_hash = hashlib.md5()
    file_hash.update(file_binary)
    return file_hash.hexdigest()

def returnHash(file_name):
    return calcHash(openFile(file_name))

# print(calcHash(openFile("9_eg_file1.txt")))
# print(returnHash("9_eg_file1.txt"))
#
# print(calcHash(openFile("9_eg_file2.txt")))
# print(returnHash("9_eg_file2.txt"))
