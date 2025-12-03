import pandas as pd
import json
import io
from googleapiclient.http import MediaIoBaseUpload
from Google import Create_Service
from information import get_information


def get_dictionary_to_json():



    information = get_information()
    for info in information:
        date_execution = info["run_timestamp_utc"]
        break
    file_name= f"OD_pair_{date_execution}.json"

    json_string = json.dumps(information, default=str)
    file_content = io.BytesIO(json_string.encode('utf-8'))

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    #print(dir(service))

    folder_id=('1ijpecM1Y60i2t18HBNRsmlW96L7Thi4N')

    mime_types='application/json'

    file_metadata={
        'name': file_name,
        'parents':[folder_id]

    }
    media =MediaIoBaseUpload(file_content,mimetype=mime_types,resumable=True)
    service.files().create(
        body=file_metadata,
        media_body= media,
        fields= 'id'
    ).execute()

if __name__ == "__main__":
    result = get_dictionary_to_json()
    print(result)