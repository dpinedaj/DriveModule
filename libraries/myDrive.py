import os
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#Local libraries
from .constants import Constants as Cts

__author__ ="Daniel Pineda"
__email__ = "dpinedaj@unal.edu.co"


class MyDrive:
#TODO implement search by mimeType
#TODO Crear decorador try-except

    """
    Class made to manage google drive from python.

    Usage:

        -> On https://console.developers.google.com
        create a google drive api service.
        -> Create credentials with the access permissions needed.
        -> Download client_secrets.json from that credentials.
        -> Put the file in config folder.
    
    """
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

    def ls(self, ar_path_id="root", ar_query = False, ar_mimetype='folder', verbose=False):
        
        if ar_mimetype in self.cts.MIMETYPES:
            mimeType = self.cts.MIMETYPES[ar_mimetype]
        else:
            print("Invalid mimeType")
            return         

        if ar_query:
            metaData = {'q': """'{0}' in parents and 
                                mimeType='{1}' and
                                trashed=false""".format(ar_path_id, mimeType)}
        else:
            metaData = {'q': """'{}' in parents and
                                trashed=false""".format(ar_path_id)}
        fileList = None
        try:
            fileList = self.drive.ListFile(metaData).GetList()
            if verbose:
                for file in fileList:
                    print('Title: %s' % (file['title']))
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

        return fileList
    
    def echo(self, ar_content, ar_name, ar_path_id='root'):

        exitValue = None
        metaData = {"title": ar_name,
                    "parents": [{
                    "kind": "drive#fileLink",
                    "id": ar_path_id}]}

        try:
            file = self.drive.CreateFile(metaData)

            file.SetContentString(ar_content)
            file.Upload()
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR
        
        return exitValue
    
    def wget(self, ar_path_id, ar_id, ar_file_path):
        exitValue = None
        metaData = {"id": ar_id,
                    "parents":[{
                    "kind": "drive#fileLink",
                    "id": ar_path_id}]}

        try:
            file = self.drive.CreateFile(metaData)
            file.GetContentFile(ar_file_path)
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

        return exitValue
            
    def get(self, ar_path_id, ar_id):

        exitValue = None
        content = None
        metaData = {"id": ar_id,
                    "parents":[{
                    "kind": "drive#fileLink",
                    "id": ar_path_id}]}

        try:
            file = self.drive.CreateFile(metaData)
            content = file.GetContentString()
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

        return content, exitValue

    def put(self, ar_file_path, ar_name, ar_path_id='root'):

        exitValue = None
        metaData = {"title": ar_name,
                    "parents": [{
                    "kind": "drive#fileLink",
                    "id": ar_path_id}]}

        try:
            file = self.drive.CreateFile(metaData)
            file.SetContentFile(ar_file_path)
            file.Upload()
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR
        
        return exitValue

    def rm(self, ar_id, ar_path_id='root'):

        exitValue = None
        metaData = {"id": ar_id,
                    "parents":[{
                    "kind": "drive#fileLink",
                    "id":ar_path_id
                    }]}

        try:
            file = self.drive.CreateFile(metaData)
            file.Trash()
            exitValue = self.cts.OK

        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR
        
        return exitValue

    def rm_per(self, ar_id, ar_path_id='root'):

        exitValue = None
        metaData = {"id": ar_id,
                    "parents":[{
                    "kind": "drive#fileLink",
                    "id":ar_path_id
                    }]}

        try:
            file = self.drive.CreateFile(metaData)
            file.Delete()
            exitValue = self.cts.OK

        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

        return exitValue
        
    def mkdir(self, ar_name, ar_path_id='root'):
        
        exitValue = None
        metaData = {"title": ar_name,
                    "parents": [{"id": ar_path_id}],
                    "mimeType": "application/vnd.google-apps.folder"}

        try:
            folder = self.drive.CreateFile(metaData)
            folder.Upload()
            exitValue = self.cts.OK
        except Exception as exc:
            print(str(exc))
            exitValue = self.cts.ERROR

        return folder['id'], exitValue 

    def mv(self):
        pass
    #TODO implement mv function


    def __repr__(self):

        return "Drive service of: {}, email: {}".format(
            self.drive.GetAbout()['user']['displayName'],
            self.drive.GetAbout()['user']['emailAddress'])
    
        