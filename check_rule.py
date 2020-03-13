import json
import config
import database_connection as db
from datetime import datetime

#Rules in the JSON file
def get_rules(rules_filename):
    try:
        with open (rules_filename, 'r') as rules:
            json_rules = rules.read()
        rules = json.loads(json_rules)
        return rules
    except Exception as ex:
        print(ex)
        return False

#funcion to check the date range
def check_date(rule_date_predicate, date_value, date_mails):
    if rule_date_predicate.lower() == 'less than':
        if datetime.now().timestamp() - date_value < date_mails:
            date_mail = True
            return date_mail
        else:
            date_mail = False
            return date_mail

    elif rule_date_predicate.lower() == 'greater than':
        if datetime.now().timestamp() - date_value > date_mails:
            date_mail = True
            return date_mail
        else:
            date_mail = False
            return date_mail
    else:
        date_mail = False
        return date_mail

#function to check the rule predicates with the mail contents
def check_predicates(mail):
        rules = get_rules(config.rules_filename)
        mail_id = mail[0]
        from_mails = mail[1]
        subject_mails = mail[2]
        date_mails = int(mail[3])
        to_mails = mail[5]
        print(mail, rules)
        for rule in rules:
            rule_name = rule['name']
            rule_details = rule['rule_details']

            if rule_details['from']['predicate'].lower() == 'contains' and rule_details['from']['string'] in from_mails:
                from_mail = True
            elif rule_details['from']['predicate'].lower() == 'does not contain' and rule_details['from']['string'] not in from_mails:
                from_mail = True
            else:
                from_mail = False

            if rule_details['date']['value']:
                rule_date_predicate = rule_details['date']['predicate']
                if rule_details['date']['type'].lower() == 'day':
                    date_value = rule_details['date']['value'] * 86400
                    date_mail = check_date(rule_date_predicate, date_value, date_mails)

                elif rule_details['date']['type'].lower() == 'month':
                    date_value = rule_details['date']['value'] * 2592000
                    date_mail = check_date(rule_date_predicate, date_value, date_mails)

            if rule_details['subject']['predicate'] == 'contains' and rule_details['subject']['string'] in subject_mails:
                subject_mail = True
            elif rule_details['subject']['predicate'] == 'does not contain' and rule_details['subject']['string'] not in subject_mails:
                subject_mail = True
            else:
                subject_mail = False

            add_labels = []
            remove_labels = []

            if rule_details['rule_predicate'].lower() == 'all':
                if from_mail and date_mail and subject_mail:
                    print('All rules met')
                    if rule['add_labels']:
                        add_labels = rule['add_labels']
                    if rule['remove_labels']:
                        remove_labels = rule['remove_labels']
                    return mail_id, add_labels, remove_labels
                else:
                    print('Rules not met')
                    return False, add_labels, remove_labels

            elif rule_details['rule_predicate'].lower() == 'any':
                if from_mail or date_mail or subject_mail:
                    print('Any rule met')
                    if rule['add_labels']:
                        add_labels = rule['add_labels']
                    if rule['remove_labels']:
                        remove_labels = rule['remove_labels']
                    return mail_id, add_labels, remove_labels
                else:
                    print('Rules not met')
                    return False, add_labels, remove_labels

#getting mails
def check_mail():
    try:
        mails = db.get_mails()
        if mails:
            for mail in mails:
                print('here')
                mail_id, add_labels, remove_labels = check_predicates(mail)
                return mail_id, add_labels, remove_labels

    except Exception as ex:
        print(ex)
        return False
