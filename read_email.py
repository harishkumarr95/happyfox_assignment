from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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

def perform_action(mail_id, mail_move_to, mail_mark_as):
    try:
        label_json = {'removeLabelIds': [], 'addLabelIds': [str(mail_move_to), str(mail_mark_as)]}

        results = service.users().messages().modify(userId='me',id = mail_id, body = label_json).execute()
        print(results)

    except Exception as identifier:
        print(identifier)

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

        for message in messages[:message_len]:
            try:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_id = msg['id']
                email_from = [ v for v in msg['payload']['headers'] if v['name'] == 'From' ][0]['value']
                email_to = [ v for v in msg['payload']['headers'] if v['name'] == 'To' ][0]['value']
                email_subject = [ v for v in msg['payload']['headers'] if v['name'] == 'Subject' ][0]['value']
                email_date = int( msg['internalDate'] )/1000
                email_message = [ v['body']['data'] for v in msg['payload']['parts'] ][0]
            except Exception as ex:
                print(ex)
            db_write = db.write_mails_to_db(email_id, email_date, email_from, email_subject, email_message, email_to)

    if db_write:
        db_write = False
        confirm_check = input( 'Would you like python to check the messages and do actions on them : (y/n)' )

        if confirm_check.lower() == 'y':
            [mail_id, (mail_move_to, mail_mark_as)] = rule.check_mail()
            if mail_id:
                action = perform_action(mail_id, mail_move_to, mail_mark_as)
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
