import json
import config
import database_connection as db

def get_rules(rules_filename):
    try:
        with open (rules_filename, 'r') as rules:
            json_rules = rules.read()
        rules = json.loads(json_rules)
        return rules
    except Exception as ex:
        print(ex)
        return False

def perform_action():
    try:
        pass
    except expression as identifier:
        pass

def check_predicates(rule_details, mails):
    for mail in mails:
        from_mails = mail[1]
        subject_mails = mail[2]
        date_mails = int(mail[3])
        to_mails = mail[5]

        if rule_details['from']['string'] in from_mails:
            from_mail = True
        else:
            from_mail = False

        if rule_details['date']['value']:
            if rule_details['date']['type'].lower() == 'day':
                date_value = rule_details['date']['value'] * 86400
                if rule_details['date']['predicate'].lower() == 'less than':
                    if date_value < date_mails:
                        date_mail = True
                    else:
                        date_mail = False
                elif rule_details['date']['predicate'].lower() == 'greater than':
                    if date_value > date_mails:
                        date_mail = True
                    else:
                        date_mail = False
                else:
                    date_mail = False

        if rule_details['subject'] in subject_mails:
            pass

def check_mail():
    try:
        rules = get_rules(config.rules_filename)
        mails = db.get_mails()
        if rules:
            for rule in rules:
                rule_name = rule['name']
                rule_details = rule['details']
                if rule_details['rule_predicate'].lower() == 'all':
                    all_predicates = check_predicates(rule_details, mails)
                    return all_predicates
                elif rule_details['rule_predicate'].lower() == 'any':
                    any_predicate = check_predicates(rule_details, mails)
                    return any_predicate
                else:
                    print('Enter a valid Predicate in the rule')
    except Exception as ex:
        print(ex)
        return False