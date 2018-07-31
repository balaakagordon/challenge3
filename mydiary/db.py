#!/usr/bin/python
import psycopg2
#from mydiary import app


class MyDiary_Database:
    def __init__(self):
        # if app.config['TESTING'] == False:
        my_db = 'mydiary_db'
        # else:
        #     my_db = 'test_db'
        try:
            # self.connect_str = "dbname='mydiary_db' user='mydiary_user' " + \
            #             "host='localhost' password='password' port='5432'"
            self.conn = psycopg2.connect(dbname=my_db, user='mydiary_user', host='localhost', password='password', port='5432')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Unable to connect. Check dbname, user or password inputs.")
            print(e)
        #self.my_db.new_entries_table
        #self.my_db.new_entries_table

    def new_users_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                    (user_id SERIAL NOT NULL PRIMARY KEY, 
                    name VARCHAR(40) NOT NULL, 
                    email VARCHAR(60) NOT NULL, 
                    password VARCHAR(40) NOT NULL);""")
        self.conn.commit()

    def new_entries_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS entries 
                    (entry_id SERIAL NOT NULL PRIMARY KEY, 
                    user_id INTEGER NOT NULL, 
                    title VARCHAR(20) NOT NULL, 
                    data VARCHAR(500) NOT NULL, 
                    date_created VARCHAR(10) NOT NULL);""")
        self.conn.commit()

# def main():
#     my_db = MyDiary_Database()
#     pass
    #users = my_db.new_entries_table
    #entries = my_db.new_entries_table
    
    
    # insert_usr_str = """INSERT INTO users (user_id, name, email, password) VALUES(%s,%s,%s,%s);"""
    # insert_ent_str = """INSERT INTO entries (entry_id, user_id, title, data, date_created) VALUES(%s,%s,%s,%s,%s);"""
    # my_db.cursor.execute(insert_usr_str, (1,"Gordon Balaaka","gb@email.com","pass1"))
    # my_db.cursor.execute(insert_usr_str, (1,"Simon Peter","sp@email.com","pass2"))
    # my_db.cursor.execute(insert_usr_str, (1,"John Bosco","jb@email.com","pass3"))
    # my_db.cursor.execute(insert_ent_str, (1,1,"First Entry","This is the first test entry","08/02/18"))
    # my_db.cursor.execute(insert_ent_str, (1,2,"Second Entry","This is the second test entry","15/03/18"))
    # my_db.cursor.execute(insert_ent_str, (1,3,"Third Entry","This is the third test entry","16/05/18"))

    # get_ent_str = """SELECT * from entries;"""
    # get_usr_str = """SELECT * from users;"""
    # my_db.cursor.execute(get_ent_str)
    # my_entries = my_db.cursor.fetchall()
    # my_db.cursor.execute(get_usr_str)
    # my_users = my_db.cursor.fetchall()
    # print(my_entries)
    # print(my_users)

# if __name__ == "__main__":
    # main()