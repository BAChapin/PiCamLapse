from global_variables import ServerSettings, DropboxSettings, GDriveSettings, \
                             GeneralSettings
from dropbox.files import WriteMode
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import dropbox
import pysftp
import sys

class Backup:

    def file(self, path: str):
        server = self.__server_backup(path)
        dropbox = self.__dropbox_backup(path)
        gdrive = self.__gdrive_backup(path)
        return server, dropbox, gdrive

    def __server_backup(self, path: str):
        if ServerSettings.enabled:
            server_home = "/home/{}".format(ServerSettings.username)

            file_name, year = self.__file_data(path)
            server_ext = "RaspiZ/{0}/{1}".format(GeneralSettings.pi_identifier,
                                                 year)

            # /home/{user_name}/RaspiZ/{Pi_Name}/{year}/{file_name}
            # This directory must be pre-constructed, or this function will fail.
            # Also note, the server I am using is Ubuntu Server 18.04.4 LTS
            # Your user directory might be different if you're using a different OS

            with pysftp.Connection(host=ServerSettings.host_address,
                                   username=ServerSettings.username,
                                   password=ServerSettings.password) as sftp:

                server_dir = "{0}/{1}".format(server_home, server_ext)

                self.__server_dir_check(sftp, server_home, server_ext)

                server_file_path = "{0}/{1}".format(server_dir, file_name)
                sftp.put(path, server_file_path)
                return server_file_path
        else:
            return ""

    def __dropbox_backup(self, path: str):
        if DropboxSettings.enabled:
            db = dropbox.Dropbox(DropboxSettings.access_token)

            file_name, year = self.__file_data(path)
            db_path = "/{}/{}/{}".format(GeneralSettings.pi_identifier,
                                      year,
                                      file_name)

            with open(path, "rb") as file:
                try:
                    db.files_upload(file.read(), db_path, mode=WriteMode("overwrite"))
                    return "DropBox:Apps/PiCamLapse/{}".format(db_path)
                except Error as err:
                    return ""
            pass
        else:
            return ""

    def __gdrive_backup(self, path: str):
        if GDriveSettings.enabled:
            gauth = self.auth_google()
            file_name, year = self.__file_data(path)
            drive, id = self.__acquire_gdrive_id(gauth, year)

            file = drive.CreateFile({"title": file_name, "parents": [{"id" : id}]})
            file.SetContentFile(path)
            file.Upload()
            return "GDrive:PiCamLapse/{}/{}/{}".format(GeneralSettings.pi_identifier, year, file_name)
        else:
            return ""

    def __file_data(self, file: str):
        separated_path = file.split("/")
        name = separated_path[-1]
        year = separated_path[-2]
        return name, year

    def __server_dir_check(self, sftp, base, remote):
        split = remote.split("/")
        builder = split[0]

        for dir in split:
            if builder is not dir:
                builder += "/{}".format(dir)

            remote_check = "{0}/{1}".format(base, builder)
            if self.__server_dir_exists(sftp, remote_check) is False:
                sftp.mkdir(remote_check)

    def __server_dir_exists(self, sftp, dir):
        return sftp.isdir(dir)

    def auth_google(self):
        gauth = GoogleAuth()
        cred_file = "{}/PiCamLapse/creds.json".format(GeneralSettings.base_path)
        gauth.LoadCredentialsFile(cred_file)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile(cred_file)

        return gauth

    def __acquire_gdrive_id(self, auth, year: str):
        # Return Year ID
        drive = GoogleDrive(auth)
        if GDriveSettings.year == year:
            return drive, GDriveSettings.year_id
        elif GDriveSettings.year == "":
            root = "PiCamLapse"
            root_id = self.__get_file_id(drive, "root", root)
            parent_id = self.__get_file_id(drive, root_id, GeneralSettings.pi_identifier)
            GDriveSettings.update_parent(parent_id)
            year_id = self.__get_file_id(drive, parent_id, year)
            GDriveSettings.update_year(year_id, year)
            return drive, year_id
        else:
            year_id = self.__get_file_id(drive, GDriveSettings.parent_id, year)
            GDriveSettings.update_year(year_id, year)
            return drive, year_id

    def __get_file_id(self, drive, id: str, file: str):
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'".format(id)}).GetList()
        for gfile in file_list:
            title = gfile["title"]
            if title == file:
                return gfile["id"]
        else:
            id = self.__create_file(drive, id, file)
            return id

    def __create_file(self, drive, id: str, name: str):
        if id == "root":
            new_file = drive.CreateFile({"title": name, "mimeType" : "application/vnd.google-apps.folder"})
            new_file.Upload()
            file_id = new_file["id"]
            return file_id
        else:
            new_file = drive.CreateFile({"title" : name, "parents" : [{"id": id}], "mimeType" : "application/vnd.google-apps.folder"})
            new_file.Upload()
            file_id = new_file["id"]
            return file_id
