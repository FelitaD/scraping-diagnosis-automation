from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import json


class GoogleSheetInterface:
    CREDS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if CREDS:
        with open(CREDS) as json_file:
            json_creds = json.load(json_file)

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
        client = gspread.authorize(creds)
