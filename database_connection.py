import mysql.connector as mysqldb

def connect_to_db():
    try:
        db_connection = mysqldb.connect(
        host = '192.168.31.220',
        user = 'root',
        passwd = 'root',
        database = 'happyfox_assignment'
        )
        cursor = db_connection.cursor()
        return db_connection, cursor
    except Exception as ex:
        print(ex)
        return False, False

def write_mails_to_db(email_id, email_date, email_from, email_subject, email_message, email_to):    
    try:
        db_connection, cursor = connect_to_db()
        if db_connection:
            query = 'CREATE TABLE IF NOT EXISTS mails ( id VARCHAR(20) NOT NULL, mail_from VARCHAR(100) NOT NULL, mail_subject VARCHAR(500) NOT NULL, mail_date INT NOT NULL, mail_message VARCHAR(10000), mail_to VARCHAR(50), is_checked INT DEFAULT 0);'
            cursor.execute(query)
            insert_query = 'INSERT INTO mails (id, mail_from, mail_subject, mail_date, mail_message, mail_to) VALUES (%s, %s, %s, %s, %s, %s);'
            values = (email_id, email_from, email_subject, email_date, email_message, email_to)
            cursor.execute(insert_query, values)
            db_connection.commit()
            db_connection.close()
            return True
        else:
            print('Database Connection lost')
            return False

    except Exception as ex:
        print(ex)
        return False

def getmails():
    try:
        db_connection, cursor = connect_to_db()
        if db_connection:
            query = 'SELECT * from mails where is_checked = 0;'
            mails = cursor.fetchall()
            db_connection.close()
            return mails
    except:
        print('Not connected')
        return False