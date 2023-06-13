import sqlite3


class Database:
    def __init__(self):
        # Establish database connection (either update current or create a new one to the designated folder path)
        self.currentDatabase = sqlite3.connect("Database/data.db")
        # Cursor object
        self.cur = self.currentDatabase.cursor()

        # Create the main table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS registers(
        id INTEGER PRIMARY KEY,
        name TEXT,
        sex TEXT,
        age INTEGER,
        total_available_time INTEGER
        )""")

        # Create the commitment activity table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS commitment_activity(
        user_id INTEGER,
        activity_name TEXT,
        activity_category TEXT,
        significant_value INTEGER,
        activity_week_duration_hours INTEGER,

        FOREIGN KEY(user_id) REFERENCES registers(id))
        """)

        # Create the leisure activity table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS leisure_activity(
        user_id INTEGER,
        activity_name TEXT,
        activity_category TEXT,
        significant_value INTEGER,
        activity_week_duration_hours INTEGER,

        FOREIGN KEY(user_id) REFERENCES registers(id))
        """)

        self.currentDatabase.commit()


    def readData(self):

        # Return all registered users
        self.cur.execute("SELECT * FROM registers")
        rows = self.cur.fetchall()
        return rows


    def deleteData(self,id):

        # Delete all the related rows first in activity tables to avoid foreign key constraint
        self.cur.execute("DELETE FROM commitment_activity WHERE user_id=?",(id,))
        self.cur.execute("DELETE FROM leisure_activity WHERE user_id=?",(id,))

        # Delete row element from the registers
        self.cur.execute("DELETE FROM registers WHERE id=?",(id,))

        self.currentDatabase.commit()



    def closeDatabase(self):

        self.cur.close()
        self.currentDatabase.close()


    def addUser(self,*args):

        self.cur.execute("INSERT INTO registers (name,sex,age,total_available_time) VALUES (?,?,?,?)",(args[0],args[1],args[2],args[3]))
        self.currentDatabase.commit()


    def addCommitmentActivity(self,user_id,*args):

        self.cur.execute("INSERT INTO commitment_activity (user_id,activity_name,activity_category,significant_value,activity_week_duration_hours) VALUES (?,?,?,?,?)",
        (user_id,args[0],args[1],args[2],args[3]))

        self.currentDatabase.commit()


    def addLeisureActivity(self,user_id,*args):

        self.cur.execute("INSERT INTO leisure_activity (user_id,activity_name,activity_category,significant_value,activity_week_duration_hours) VALUES (?,?,?,?,?)",
        (user_id, args[0], args[1], args[2], args[3]))

        self.currentDatabase.commit()


    def primaryKeyData(self,primary):

        self.cur.execute("""SELECT * 
        FROM registers WHERE id=?""", (primary,))
        registersData = self.cur.fetchone()

        self.cur.execute("""SELECT * 
        FROM leisure_activity
        WHERE user_id=?""", (primary,))
        leisureData = self.cur.fetchall()

        self.cur.execute("""SELECT * 
        FROM commitment_activity
        WHERE user_id=?""", (primary,))
        commitmentData = self.cur.fetchall()

        return registersData,leisureData,commitmentData


    def updateDatabase(self,category,user_id,name,*args):

        if category:
            # Commitment
            self.cur.execute('''UPDATE commitment_activity 
            SET activity_name = ?,
                activity_category = ?,
                significant_value = ?,
                activity_week_duration_hours = ?

                WHERE activity_name = ? AND user_id = ?
                ''',(args[0],args[1],args[2],args[3],name,user_id))

        else:
            # Leisure
            self.cur.execute('''UPDATE leisure_activity 
            SET activity_name = ?,
                activity_category = ?,
                significant_value = ?,
                activity_week_duration_hours = ?

                WHERE activity_name = ? AND user_id = ?
                ''',(args[0],args[1],args[2],args[3],name,user_id))

        self.currentDatabase.commit()



    def changeActivity(self,category,user_id,name,*newActivity):

        # First delete the activity, then add it to the other table
        if category == 0:
            self.cur.execute("""DELETE FROM leisure_activity
            WHERE user_id = ? AND activity_name = ?
            """,(user_id,name))

            self.addCommitmentActivity(user_id, *newActivity)


        # Other case
        else:
            # Now we want to delete from commitment table and add to the other
            self.cur.execute("""DELETE FROM commitment_activity
            WHERE user_id = ? AND activity_name = ?
            """, (user_id, name))

            self.addLeisureActivity(user_id,*newActivity)

        self.currentDatabase.commit()



    def deleteSpecificActivity(self,category,user_id,name):

        if category == 0:
            self.cur.execute("""DELETE FROM leisure_activity
            WHERE user_id = ? AND activity_name = ?
            """,(user_id,name))

        else:
            self.cur.execute("""DELETE FROM commitment_activity
            WHERE user_id = ? AND activity_name = ?
            """, (user_id, name))

        self.currentDatabase.commit()



    def calculateData(self,user_id):

        meanCommitment = 0.0
        meanLeisure = 0.0
        timeCommitment = 0
        timeLeisure = 0

        re,le,co = self.primaryKeyData(user_id)

        if not le:
            pass
        else:
            for tup in le:
                timeLeisure += tup[4]

            meanLeisure = round(timeLeisure / len(le),2)


        if not co:
            pass
        else:
            for tup in co:
                timeCommitment += tup[4]

            meanCommitment = round(timeCommitment / len(co),2)

        return meanCommitment,meanLeisure,timeCommitment,timeLeisure