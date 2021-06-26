from pydrive.auth import GoogleAuth

if __name__ == "__main__":
    gauth = GoogleAuth()
    cred_file = "creds.json"
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile(cred_file)