import sys
import os
import time
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.myDrive import MyDrive
from modules.tasksManager import TaskManager
from modules.db_session import session


drive = MyDrive()
folders = pd.DataFrame(columns=['title', 'src', 'dst'])


for folder in drive.ls():
    if folder['title'] == 'CD_T1':
        baseFolderId,_ = drive.mkdir(folder['title'] + '_COPY', ar_path_id='root')
        sourceFolderId = folder['id']
        folders = folders.append({'title':folder['title'],'src':sourceFolderId, 'dst': baseFolderId},
                            ignore_index=True)



try:
    with open('out/lastValue.txt', 'r') as f:
        t = int(f.read())
except:
    t = 1

n = 0
while True:
    try:
        folder = folders.iloc[n]
        newPath = drive.ls(folder.src)
        if len(newPath) > 0:
            for file in newPath:
                if file['mimeType'] != 'application/vnd.google-apps.folder':
                    exists = drive.check(folder.dst, file['title'])
                    
                    if not exists:
                        taskManager = TaskManager(
                            pid = t,
                            id = file['id'],
                            title = file['title'],
                            source = folder.src, 
                            destiny = folder.dst,
                            fails=False,
                            processing=False,
                            error = ' '
                        )
                        session.add(taskManager)
                        session.commit()
                        
                        print('loading task {}, file {}'.format(t, file['title']))
                        t += 1
                else:
                    newFolderId, _ = drive.mkdir(file['title'], ar_path_id=folder.dst)
                    folders = folders.append({'title':file['title'],'src':file['id'], 'dst': newFolderId},
                                    ignore_index=True)
    
        n += 1
    except KeyboardInterrupt:
        with open('out/lastValue.txt', 'w') as f:
            f.write(str(t))
        sys.exit()

    except Exception as exc:
        print(str(exc))
        folders.drop(folders.index, inplace=True)
        folders = folders.append({'src':sourceFolderId, 'dst': baseFolderId},
                            ignore_index=True)
        n = 0
        time.sleep(30)