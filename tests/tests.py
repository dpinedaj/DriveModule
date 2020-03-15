import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.myDrive import MyDrive
drive = MyDrive()

for i in drive.ls():
    if i['title'] == 'Pruebas1':
        pruebasId = i['id']
        break

for i in range(100):
    drive.echo('Hola', f'prueba_{i}.txt', pruebasId)

for i in drive.ls(pruebasId):
    localPath = os.path.join('pruebas', i['title'])
    drive.wget(pruebasId,i['id'], localPath)
    drive.rm_per(i['id'], pruebasId)
