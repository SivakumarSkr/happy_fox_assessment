import datetime
import re
import psycopg2
import os
from dateutil.relativedelta import relativedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_relative_date(value):
    regex = r"(\d+) (days|months){1} old"
    result = re.search(regex, value).groups()
    args = {result[1]: int(result[0])}
    return datetime.datetime.today() - relativedelta(**args)


def convert_to_date(field_value):
    return datetime.datetime.fromtimestamp(int(field_value)//1000)


class BaseClass:
    
    def __init__(self):
        self.db_connection = self.get_db_connection()
        self.table_name = os.getenv('GMAIL_TABLE_NAME')
        self.service = self.read_credentials()

    def read_credentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        return service

    def get_db_connection(self):
        return psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD')
        )