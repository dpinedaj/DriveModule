import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.myDrive import MyDrive
from modules.tasksManager import TaskManager


drive = MyDrive()
folders = dict()


for folder in drive.ls():
    if folder['title'] == 'CD_T1':
        newFolderId,_ = drive.mkdir(folder['title'], ar_path_id='root')
        folders[folder['title']] = [folder['id'], newFolderId]


for folder in folders.keys():
    newPath = drive.ls(folder[0])
    if len(newPath) > 0:
        for file in newPath:
            if file['mimeType'] != 'application/vnd.google-apps.folder':

                taskManager = TaskManager(
                    title = file['title'],
                    id = file['id'],
                    source = folder[0], 
                    destiny = folder[1],
                    fails=False,
                    processing=False,   
                    error = ' '
                )

            else:
                newFolderId, _ = drive.mkdir(file['title'], ar_path_id=folder[1])
                folders[file['title']] = [file['id'], newFolderId]
        

        del folders[folder['title']]

