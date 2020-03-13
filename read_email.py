from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors

import database_connection as db

import check_rule as rule

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'

#SCOPES = 'https://mail.google.com/'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

#To perform the rule actions 
def perform_action(mail_id, add_labels, remove_labels):
    try:

        label_json = { }

        if len(add_labels) != 0:
            label_json['addLabelIds'] = []
            label_json['addLabelIds'] = add_labels
        if len(remove_labels) != 0:
            label_json['removeLabelIds'] = []
            label_json['removeLabelIds'] = remove_labels
        if label_json:
            results = service.users().messages().modify(userId='me',id = mail_id, body = label_json).execute()
            print(results)
            return True
        else:
            print('Add some actions to perform')
            return False

    except errors.HttpError as error:
        print(error)
        return False

def main():
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])


    if not messages:
        print("No messages found.")
    else:
        print("Total messages :", len(messages))

        try:
            message_len = input('Enter number of messages you would like to fetch : ')
            if message_len.isdigit():
                message_len = int(message_len)
            else:
                print('Enter an Integer')
                return
        except Exception as ex:
            print('Error', ex)
            return

        db_write = False

        #from the message list storing to database
        for message in messages[:message_len]:
            try:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_id = msg['id']
                email_from = [ v for v in msg['payload']['headers'] if v['name'] == 'From' ][0]['value']
                email_to = [ v for v in msg['payload']['headers'] if v['name'] == 'To' ][0]['value']
                email_subject = [ v for v in msg['payload']['headers'] if v['name'] == 'Subject' ][0]['value']
                email_date = int( msg['internalDate'] )/1000
                try:
                    email_message = [ v['body']['data'] for v in msg['payload']['parts'] ][0]
                except KeyError:
                    email_message = msg['payload']['body']['data']
            except Exception as ex:
                print(ex)
            db_write = db.write_mails_to_db(email_id, email_date, email_from, email_subject, email_message, email_to)

    #checking the mails for the rules
    if db_write:
        db_write = False
        confirm_check = input( 'Would you like python to check the messages and do actions on them : (y/n)' )

        if confirm_check.lower() == 'y':
            mail_id, add_labels, remove_labels = rule.check_mail()
            if mail_id:
                action = perform_action(mail_id, add_labels, remove_labels)
                if action:
                    print('Mail moved Successfully')
                    return
                else:
                    print('Mail not moved, Please try again')
                    return
        elif confirm_check.lower() == 'n':
            print("Your mails have been stored successfully")
            return
        else:
            print('Enter a valid option')
            return

if __name__ == '__main__':
    main()
