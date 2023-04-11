import sqlite3


class Database:
    def __init__(self):
        # establish database connection (either update current or create a new one to the designated folder path)
        self.currentDatabase = sqlite3.connect("Database/data.db")
        # cursor object
        self.cur = self.currentDatabase.cursor()

        #create the main table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS registers(
        id INTEGER PRIMARY KEY,
        name TEXT,
        sex TEXT,
        age INTEGER
        )""")

        #create the commitment activity table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS commitment_activity(
        user_id INTEGER,
        activity_name TEXT,
        activity_category TEXT,
        significant_value INTEGER,
        activity_week_duration_hours INTEGER,
        available_hours_per_week INTEGER,
        FOREIGN KEY(user_id) REFERENCES registers(id))
        """)

        #create the leisure activity table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS leisure_activity(
        user_id INTEGER,
        activity_name TEXT,
        activity_category TEXT,
        significant_value INTEGER,
        activity_week_duration_hours INTEGER,
        available_hours_per_week INTEGER,
        FOREIGN KEY(user_id) REFERENCES registers(id))
        """)

        self.currentDatabase.commit()


    def readData(self):
        #choose all elements in a row
        self.cur.execute("SELECT * FROM registers")
        rows = self.cur.fetchall()
        return rows

    def deleteData(self,id):

        #delete all the related rows first in activity tables to avoid foreign key constraint
        self.cur.execute("DELETE FROM commitment_activity WHERE user_id=?",(id,))
        self.cur.execute("DELETE FROM leisure_activity WHERE user_id=?",(id,))

        #delete an element from the registers
        self.cur.execute("DELETE FROM registers WHERE id=?",(id,))

        #delete all the related rows in activity tables
        self.cur.execute("DELETE FROM commitment_activity WHERE user_id=?",(id,))
        self.cur.execute("DELETE FROM leisure_activity WHERE user_id=?",(id,))

        self.currentDatabase.commit()



    def closeDatabase(self):
        self.cur.close()
        self.currentDatabase.close()


    def addUser(self,*args):

        self.cur.execute("INSERT INTO registers (name,sex,age) VALUES (?,?,?)",(args[0],args[1],args[2]))
        self.currentDatabase.commit()


    def addCommitmentActivity(self,user_id,*args):

        self.cur.execute("INSERT INTO commitment_activity (user_id,activity_name,activity_category,significant_value,activity_week_duration_hours,available_hours_per_week) VALUES (?,?,?,?,?,?)",
        (user_id,args[0],args[1],args[2],args[3],args[4]))

        self.currentDatabase.commit()

    def addLeisureActivity(self,user_id,*args):
        self.cur.execute("INSERT INTO leisure_activity (user_id,activity_name,activity_category,significant_value,activity_week_duration_hours,available_hours_per_week) VALUES (?,?,?,?,?,?)",
        (user_id, args[0], args[1], args[2], args[3], args[4]))

        self.currentDatabase.commit()