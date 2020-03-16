#!/usr/bin/python
import sys
import os


class Constants:


    def __init__(self):
        self.__OK = 0
        self.__FAIL = 1
        self.__ERROR = -1
        self.__NODATA = 100
        self.__GLOBALCONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config","globalConfig.properties")
        self.__DB_URL = 'postgresql://admin:admin@localhost:5432/pruebas'
        self.__CREDPATH = '/home/daniel/Desktop/actualProject/cargasDrive/config'
        self.__CREDNAME = 'credentials.json'
        self.__SECNAME = 'client_secrets.json'
        self.__MIMETYPES = {
                                "xls" :'application/vnd.ms-excel',
                                "xlsx" :'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                "xml" :'text/xml',
                                "ods":'application/vnd.oasis.opendocument.spreadsheet',
                                "csv":'text/plain',
                                "tmpl":'text/plain',
                                "pdf": 'application/pdf',
                                "php":'application/x-httpd-php',
                                "jpg":'image/jpeg',
                                "png":'image/png',
                                "gif":'image/gif',
                                "bmp":'image/bmp',
                                "txt":'text/plain',
                                "doc":'application/msword',
                                "js":'text/js',
                                "swf":'application/x-shockwave-flash',
                                "mp3":'audio/mpeg',
                                "zip":'application/zip',
                                "rar":'application/rar',
                                "tar":'application/tar',
                                "arj":'application/arj',
                                "cab":'application/cab',
                                "html":'text/html',
                                "htm":'text/html',
                                "default":'application/octet-stream',
                                "folder":'application/vnd.google-apps.folder'}

    @property
    def OK(self):

        return self.__OK

    @property
    def ERROR(self):

        return self.__ERROR

    @property
    def NODATA(self):

        return self.__SINDATOS

    @property
    def FAIL(self):

        return self.__FALLO

    @property
    def GLOBALCONFIG(self):

        return self.__GLOBALCONFIG
   
    @property
    def DB_URL(self):

        return self.__DB_URL

    @property
    def CREDPATH(self):

        return self.__CREDPATH
    
    @property
    def CREDNAME(self):

        return self.__CREDNAME
    
    @property
    def SECNAME(self):

        return self.__SECNAME

    @property
    def MIMETYPES(self):

        return self.__MIMETYPES




        
        
        