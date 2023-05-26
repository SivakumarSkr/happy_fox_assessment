import psycopg2
import psycopg2.extras
import json
from rule_collection import RuleCollection
from googleapiclient.errors import HttpError
from utils import BaseClass


class EmailProcessor(BaseClass):
    """Class for loading emails from database and apply rules for actions"""
    RULE_FILE_NAME = "rule.json"

    def read_emails_from_db(self):
        """Read emails from database."""
        emails = []
        try:
            self.db_connection.autocommit = True
            cursor = self.db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = f'SELECT * FROM {self.table_name}'
            cursor.execute(query)
            emails = cursor.fetchall()

        except (Exception, psycopg2.Error) as e:
            print("Error while read emails from the db", e)
        finally:
            if self.db_connection:
                cursor.close()
                self.db_connection.close()
        return emails

    def serialize_rule_set(self):
        """Read rule file and serialize it"""
        try:
            with open(self.RULE_FILE_NAME) as f:
                rules = json.load(f)
            return RuleCollection(rules)
        except FileNotFoundError as e:
            raise Exception(f"{self.RULE_FILE_NAME} not found in the directory")

    def add_or_remove_labels(self, message_ids, params):
        """By using gmail API's label update feature
        """
        try:
            return self.service.users().messages().batchModify(
                userId='me',
                body={
                    'ids': message_ids,
                    **params
                }
            ).execute()
        except HttpError as e:
            print(f'Error occured from gmail API while update labels {e}')

    
    def apply_actions(self, email_ids, rule_set):
        """"Applying actions specified in rules to selected emails. 
        This implementation does not adhere to the open-closed principle and requires an update."
        """
        actions = rule_set.actions
        params = {
            "removeLabelIds": [],
            "addLabelIds": []
        }
        for action in actions:
            if action['name'] == 'mark_as_read':
                params['removeLabelIds'].append('UNREAD')
            elif action['name'] == 'mark_as_unread':
                params['addLabelIds'].append('UNREAD')
            elif action['name'] == 'move':
                destination = action['destination']
                params['addLabelIds'].append(destination)
            else:
                raise ValueError(f"Invalid action {action['name']}")
        self.add_or_remove_labels(email_ids, params)

    def apply_rules(self):
        """main method of class"""
        emails = self.read_emails_from_db()
        rule_set = self.serialize_rule_set()
        emails_to_apply = list(filter(lambda x: rule_set.verify(x), emails))
        email_ids = [email["email_id"] for email in emails_to_apply]
        self.apply_actions(email_ids, rule_set)
    

email_processor = EmailProcessor()
email_processor.apply_rules()