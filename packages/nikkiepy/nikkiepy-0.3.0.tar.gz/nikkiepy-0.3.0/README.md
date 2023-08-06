# nikkiepy
Custom python library

## Current features

### Sockets
* connection_test(host=host, port=port)

##### Examples:
###### `connection_test(host="127.0.0.1", port=5000)` Output: ```Connects and inmediately disconnects from host, used to test connection```
##### Notes:
###### * None *for now*

### files
* mkfile(path, name, extension)
* delfile(file)
* delfolder(folder)
* readfile(file)

##### Examples:
###### `mkfile(path="E:/coding/testing/python", name="testfile", extension="txt")` Output: ```File: testfile.txt has been made in E:/coding/testing/python```
###### `delfile(file="E:/coding/testing/python/testfile.txt")` Output: ```File: testfile.txt successfully deleted!```
###### `delfolder(folder="E:/coding/testing")` Output: ```Folder: testing has been successfully deleted!```
###### `readfile(file="file.txt")` Output: ```The contents of file.txt```
##### Notes:
###### * None *for now*

### crypt
* encrypt(file)
* decrypt(file)

##### Examples:
###### `encrypt(file="E:/Coding/testing/python/file.txt")`
###### `decrypt(file="E:/Coding/testing/python/file.txt")`
##### Notes:
###### * None *for now*


# CREATED BY NikkieDev
## Discord: Nikkiedev#6322
## Business contact: nikkieschaad@gmail.com

### Libraries:
* os
* socket
* cryptography.fernet
