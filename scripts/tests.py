import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.myDrive import MyDrive

drive = MyDrive()
content = 'HOLA MAMAAAAAA'
name = 'testingUpload.txt'
print(drive.echo(content,name))