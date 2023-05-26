from __future__ import print_function
import base64
import psycopg2
from dotenv import load_dotenv

from utils import BaseClass
from googleapiclient.errors import HttpError

load_dotenv()


class EmailFetcher(BaseClass):
    """Class for fetching emails from gmail and store in database"""

    # This class only needs readonly permission
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    # order of fields needed while inserting
    FIELD_ORDER = ('email_id', 'subject', 'from_email', 'received_date', 'message')

    def load_emails_to_db(self):
        """entry method to this class"""
        emails = self.get_emails_from_gmail()
        self.create_table_if_not_present()
        populated_msgs = [self.populate_email(email) for email in emails]
        self.insert_bulk_to_db(populated_msgs)

    def get_emails_from_gmail(self):
        """This method will fetch emails from gmail api. restricted by date query."""
        try:
            results = self.service.users().messages().list(
                userId='me', labelIds=['INBOX'], q="after:05/01/2023").execute()
        except HttpError as e:
            print(f"An error occured from gmail API while fetching emails: {e}")
        messages = results.get('messages', [])
        return messages

    def create_table_if_not_present(self):
        """create table for store emails if not present."""
        try:
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id SERIAL PRIMARY KEY,
                    email_id TEXT NOT NULL,
                    subject TEXT,
                    from_email TEXT,
                    received_date TEXT,
                    message TEXT
                )
            """
            with self.db_connection.cursor() as cursor:
                cursor.execute(create_table_query)
            self.db_connection.commit()
        except (psycopg2.Error) as e:
            raise Exception("Error from database while creating the table")

    def get_value_from_header(self, headers, key):
        """return value from headers"""
        for header in headers:
            if header['name'] == key:
                return header['value']
        else:
            return ""

    def get_emails_content(self, payload):
        """read and decode email content"""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        return ''

    def populate_email(self, message):
        """create a tuple of a email with required data by calling gmail api"""
        try:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            return (
                message['id'],
                self.get_value_from_header(msg["payload"]["headers"], "Subject"),
                self.get_value_from_header(msg["payload"]["headers"], "From"),
                # storing date time as epoch value
                msg["internalDate"],
                self.get_emails_content(msg["payload"])
            )
        except KeyError as e:
            raise ValueError(f"Couldn't get {e.args} value from email data while populate.")
        except HttpError as e:
            print(f'Error occurred while populating the email {e}')
    
    def insert_bulk_to_db(self, emails):
        """bulk inserting populated emails to db."""
        try:
            cursor = self.db_connection.cursor()
            arg_string = f'({",".join(["%s"] * len(self.FIELD_ORDER))})'
            args = ','.join(cursor.mogrify(arg_string, i).decode('utf-8')
                    for i in emails)
            colum_names = f"({','.join(self.FIELD_ORDER)})"
            cursor.execute(f"INSERT INTO {self.table_name} {colum_names} VALUES " + (args))
        except (Exception, psycopg2.Error) as e:
            print("Error while insert to db", e)
        finally:
            self.db_connection.commit()
            self.db_connection.close()


email_fetcher = EmailFetcher()
email_fetcher.load_emails_to_db()