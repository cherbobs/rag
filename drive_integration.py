from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Chemin vers votre fichier JSON du compte de service
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Authentification
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def list_drive_files():
    """Lister les fichiers accessibles par le compte de service"""
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    files = results.get('files', [])
    if not files:
        print("Aucun fichier accessible pour ce compte.")
        return []
    else:
        print("Fichiers accessibles :")
        for file in files:
            print(f"{file['name']} ({file['id']})")
    return files

def download_file(file_id, file_name):
    """Télécharger un fichier de Google Drive"""
    request = service.files().get_media(fileId=file_id)
    with open(file_name, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
