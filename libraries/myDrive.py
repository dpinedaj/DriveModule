import os
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#Local libraries
from .constants import Constants as Cts


class MyDrive:

    def __init__(self, ar_cred_file=None, ar_secret_file=None):

        self.cts = Cts()
        self.gauth = self.__connect(ar_cred_file, ar_secret_file)
        self.drive = GoogleDrive(self.gauth)
        
    def __connect(self, ar_cred_file, ar_secret_file):
        
        credFile = ar_cred_file
        secFile = ar_secret_file
        exitValue = None

        try:
            if credFile is None:
                credFile = self.cts.CREDNAME
            if secFile is None:
                secFile = self.cts.SECNAME
            
            gauth = GoogleAuth()
            credPath = os.path.join(self.cts.CREDPATH, credFile)
            secPath = os.path.join(self.cts.CREDPATH, secFile)
            gauth.LoadCredentialsFile(credPath)
            if gauth.credentials is None:
                gauth.LocalWebserverAuth(secPath)
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
            gauth.SaveCredentialsFile(os.path.join(self.cts.CREDPATH, self.cts.CREDNAME))

        except Exception as exc:
            print(str(exc))

        return gauth

    def ls(self, ar_path_id="root", verbose=False):

        try:
            fileList = self.drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format(ar_path_id)}
                ).GetList()
            if verbose:
                for file in fileList:
                    print('Title: %s, ID: %s' % (file['title'], file['id']))
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR
        return fileList
    
    def echo(self, ar_content, ar_name, ar_path_id='root'):

        exitValue = None
        try:
            file = self.drive.CreateFile({"title": ar_name,
                                        "parents": [{
                                        "kind": "drive#fileLink",
                                        "id": ar_path_id}]})

            file.SetContentString(ar_content)
            file.Upload()
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR
        
        return exitValue
    
    def wget(self, ar_path_id, ar_id, ar_file_path):
        exitValue = None
        try:
            file = self.drive.CreateFile({"id": ar_id,
                                        "parents":[{
                                        "kind": "drive#fileLink",
                                        "id": ar_path_id}]})
            file.GetContentFile(ar_file_path)
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

        return exitValue
            
    def get(self, ar_path_id, ar_id):

        exitValue = None
        content = None
        try:
            file = self.drive.CreateFile({"id": ar_id,
                                        "parents":[{
                                        "kind": "drive#fileLink",
                                        "id": ar_path_id}]})
            content = file.GetContentString()
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

        return content, exitValue

    def put(self, ar_file_path, ar_name, ar_path_id='root'):

        exitValue = None
        try:
            file = self.drive.CreateFile({"title": ar_name,
                                    "parents": [{
                                    "kind": "drive#fileLink",
                                    "id": ar_path_id}]})
            file.SetContentFile(ar_file_path)
            file.Upload()
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR
        
        return exitValue

    def rm(self, ar_id, ar_path_id='root'):

        exitValue = None

        try:
            file = self.drive.CreateFile({"id": ar_id,
                                        "parents":[{
                                        "kind": "drive#fileLink",
                                        "id":ar_path_id
                                        }]})
            file.Trash()
            exitValue = self.cts.OK

        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

    def rm_per(self, ar_id, ar_path_id='root'):

        exitValue = None

        try:
            file = self.drive.CreateFile({"id": ar_id,
                                        "parents":[{
                                        "kind": "drive#fileLink",
                                        "id":ar_path_id
                                        }]})
            file.Delete()
            exitValue = self.cts.OK

        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR
    
        