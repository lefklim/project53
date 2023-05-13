# Modifiable file 3

from tkinter import *
from PIL import Image,ImageTk
import sqlite3
from database import Database
import matplotlib.pyplot as plt
import matplotlib

# Κυρίως χρώμα για το background
basicColor = "#0076cc"

WIDTH = 1280
HEIGHT = 720

# This is used for rescaling the background image
IMAGESIZE = (WIDTH,HEIGHT)

# Starting menu
class app(Database):

    # With this variable we keep track of the primary key
    primaryKey = 0

    graphData = ''

    # Flag to know if an activity is commitment or leisure (1 or 0 respectively)
    activityCategory = None
    chosenActivity = None

    newActivityData = []
    registeredUser = []
    commitmentActivityData = []
    leisureActivityData = []
    temporaryDataList = []
    userLabels = []

    def __init__(self):
        Database.__init__(self)
        self.entryWindow = Tk()
        self.entryWindow.resizable(False,False)
        self.entryWindow.title("TimeManager")


        # We store the address of the images
        self.background = Image.open('Images/background.png')
        self.favicon = PhotoImage(file="Images/logo.png")
        self.left = Image.open('Images/left.png')
        self.right = Image.open('Images/right.png')
        self.userLogo = Image.open('Images/userlogo.png')
        self.dataLogo = Image.open('Images/database.png')
        self.welcomeIcon = Image.open('Images/taskbaricon.ico')
        self.welcomeIcon = ImageTk.PhotoImage(self.welcomeIcon)
        self.graphIcon = Image.open('Images/graph.png')
        # Adjusting and Compatibility (for tkinter)
        self.background = self.background.resize(IMAGESIZE)
        self.background = ImageTk.PhotoImage(self.background)
        self.left = self.left.resize((100,100))
        self.right = self.right.resize((100,100))
        self.left = ImageTk.PhotoImage(self.left)
        self.right = ImageTk.PhotoImage(self.right)
        self.userLogo = self.userLogo.resize((50,50))
        self.userLogo = ImageTk.PhotoImage(self.userLogo)
        self.dataLogo = self.dataLogo.resize((30,30))
        self.dataLogo = ImageTk.PhotoImage(self.dataLogo)
        self.graphIcon = self.graphIcon.resize((40,40))
        self.graphIcon = ImageTk.PhotoImage(self.graphIcon)
        # Favicon image
        self.entryWindow.iconphoto(False, self.favicon)

        # Initializing
        self.mainMenu()



######### Main Menu #########
    def mainMenu(self):

        # Creating the main frame widget into self.entryWindow
        self.introFrame = Frame(self.entryWindow,width=WIDTH,height=HEIGHT)
        self.introFrame.pack()

        # Putting an image into the frame
        self.backgroundImage = Label(self.introFrame,image=self.background)
        self.backgroundImage.place(x=0,y=0,relheight=1,relwidth=1)

        # Putting the welcoming label
        self.welcome = Label(self.backgroundImage,bg="#99ccff",bd=2,relief='solid')
        self.welcome.place(relx=0.3,rely=0.1,relheight=0.2,relwidth=0.4)

        self.leftLabel = Label(self.welcome,padx=30,font=('TkHeadingFont', 25),text="Καλώς Ήρθατε!",fg='#003380',image=self.welcomeIcon,compound='left',bg="#99ccff")
        self.leftLabel.place(rely=0.35,relx=0.11)

        self.rightLabel = Label(self.welcome,image=self.welcomeIcon,bg="#99ccff")
        self.rightLabel.place(rely=0.42,relx=0.77)




        # Buttons attached to the intro window (ontop of the image)
        self.insertButton = Button(self.backgroundImage,font=('TkHeadingFont',15),cursor="hand2", text="Εισαγωγή",bd=3, command=self.insert)
        self.insertButton.place(relx=0.62,rely=0.8)

        self.modifyButton = Button(self.backgroundImage,font=('TkHeadingFont',15),cursor="hand2", text="Τροποποίηση",bd=3, command=self.modify)
        self.modifyButton.place(relx=0.44,rely=0.8)

        self.deleteButton = Button(self.backgroundImage,font=('TkHeadingFont',15),cursor="hand2", text="Διαγραφή",bd=3, command=self.delete)
        self.deleteButton.place(relx=0.28,rely=0.8)

        self.registerButton = Button(self.backgroundImage,font=('TkHeadingFont',30),cursor="hand2", text="Χρήστες",padx=15,bd=3,image=self.userLogo,compound="left", command=self.registeredUsers)
        self.registerButton.place(relx=0.39,rely=0.4,relheight=0.2,relwidth=0.2)



    # Getting Access to the database (User's Menu)
    def registeredUsers(self):

        # Resetting
        self.graphData = ''
        self.userLabels.clear()
        self.leisureActivityData.clear()
        self.commitmentActivityData.clear()
        self.chosenActivity = None
        self.activityCategory = None


        # Destroying the previous frame
        self.introFrame.destroy()

        # RegisteredUsers frame initialized
        self.registeredUsersFrame = Frame(self.entryWindow,width=WIDTH,height=HEIGHT,bg=basicColor)
        self.registeredUsersFrame.pack()


        self.position = 0.03
        labelsText=['Ονοματεπώνυμο', 'Φύλο', 'Ηλικία','Συνολικός Χρόνος', 'Δραστηριότητα', 'Κατηγορία', 'Βαθμός Σημαντικότητας', 'Διάρκεια ανά Εβδομάδα(ώρες)'
                             ,'Απαιτούμενος Χρόνος Ελεύθερων','Απαιτούμενος Χρόνος Υποχρεώσεων','Mean Ελεύθερων','Mean Υποχρεώσεων']

        for data in labelsText:
            Label(self.registeredUsersFrame,relief="groove",borderwidth=2,font=('TkHeadingFont', 15),text=data,bg="#99ccff").place(relx=0.04,rely=self.position,relwidth=0.31,relheight=0.05)
            self.position += 0.07

        self.position = 0.03
        for num in range(12):
            self.userLabels.append(Label(self.registeredUsersFrame,relief="groove",font=('TkHeadingFont', 15)))
            self.userLabels[num].place(relx=0.4, rely=self.position, relwidth=0.31, relheight=0.05)
            self.position += 0.07

        # Button that fetches data from the database file
        self.databaseButton = Button(self.registeredUsersFrame, font=('TkHeadingFont',15), cursor='hand2', text="Καταχωρημένοι", bd=3, command=lambda :self.fetchingData(self.userLabels))
        self.databaseButton.place(relx=0.80,rely=0.1,relwidth=0.15,relheight=0.1)

        # Button that goes to the activities section
        self.possibleActivityButton = Button(self.registeredUsersFrame, font=('TkHeadingFont', 15), cursor='hand2', text="Εφικτές", bd=3,command=self.possibleActivitiesMenu)
        self.possibleActivityButton.place(relx=0.80, rely=0.3, relwidth=0.15, relheight=0.1)

        # Button that returns to the homepage
        self.homeButton = Button(self.registeredUsersFrame,font=('TkHeadingFont',15),cursor='hand2',text="Αρχική",bd=3,command=self.returnHomeFromUsers)
        self.homeButton.place(relx=0.80,rely=0.7,relwidth=0.15,relheight=0.1)

        # Activity button
        self.activityRegisteredButton = Button(self.registeredUsersFrame,font=('TkHeadingFont',15),cursor='hand2',text="Δραστηριότητα",bd=3,command=self.activityProceedCheck)
        self.activityRegisteredButton.place(relx=0.8,rely=0.5,relwidth=0.15,relheight=0.1)


    def graphFunction(self,totaltime,lei,com):

        if not lei and not com: return

        matplotlib.rcParams['figure.figsize'] = [10.0, 6.0]
        fig, ax = plt.subplots(nrows=1, ncols=2)
        plt.suptitle('Αναπαράσταση Δεδομένων')

        # Leisure
        if len(lei) != 0:
            leiData = [lei[i][1] for i in range(len(lei))]
            leiTime = [100.0*((float)(lei[i][4])/(totaltime)) for i in range(len(lei))]
            ax[0].bar(leiData, leiTime)
            ax[0].set_title("Δραστηριότητες Ελεύθερων")
            ax[0].set_ylabel("Χρόνος % (του συνολικού)")

        # Commitment
        if len(com) != 0:
            comData = [com[i][1] for i in range(len(com))]
            comTime = [100.0*((float)(com[i][4])/(totaltime)) for i in range(len(com))]
            ax[1].bar(comData, comTime, color='#ff6600')
            ax[1].set_title("Δραστηριότητες Υποχρεώσεων")
            ax[1].set_ylabel("Χρόνος % (του συνολικού)")

        plt.show()




## Being built ##
    def possibleActivitiesMenu(self):

        if not self.graphData:
            return

        self.leiGraph = []
        self.comGraph = []
        # Temporary variables for the commitment and leisure activities
        reg,lei,com = self.primaryKeyData(self.graphData[0])



        #Creating the new frame
        self.registeredUsersFrame.destroy()
        self.possibleActivityFrame = Frame(self.entryWindow,width=WIDTH,height=HEIGHT,bg=basicColor)
        self.possibleActivityFrame.pack()

        Label(self.possibleActivityFrame,relief="groove",borderwidth=2,font=('Times',20),bg="#99ccff",text="Δραστηριότητες με φθίνουσα σημαντικότητα και εντός\nτου συνολικού διαθέσιμου χρόνου του Χρήστη ({} ώρες)".format(self.graphData[4])).place(relx=0.25,rely=0.03)

        self.homePossibleButton = Button(self.possibleActivityFrame,font=('TkHeadingFont',15),cursor='hand2',text="Αρχική",bd=3,command=lambda :self.returnHomeFromUsers(1))
        self.homePossibleButton.place(relx=0.75,rely=0.80,relwidth=0.15,relheight=0.1)

        self.graphButton = Button(self.possibleActivityFrame,font=('TkHeading',15),cursor='hand2',image=self.graphIcon,compound='left',padx=10,text="Γράφημα",bd=3,command=lambda :self.graphFunction(reg[4],self.leiGraph,self.comGraph))
        self.graphButton.place(relx=0.10, rely=0.80,relwidth=0.15,relheight=0.1)

        # Commitment table
        self.commitmentFrame = Frame(self.possibleActivityFrame,bg='white',highlightthickness=2, highlightbackground="#00ccff")
        self.commitmentFrame.place(relx=0.07,rely=0.15,relheight=0.6,relwidth=0.4)

        Label(self.commitmentFrame,text="Υποχρεώσεων",font=('Times',20)).pack()

        self.scrollbarCommitment = Scrollbar(self.commitmentFrame)
        self.scrollbarCommitment.pack(side=RIGHT,fill=Y)
        self.listboxCommitment = Listbox(self.commitmentFrame,font=('TkHeading',15),yscrollcommand=self.scrollbarCommitment.set)
        self.listboxCommitment.pack(side=LEFT, fill=BOTH, expand=1)


        # Leisure table
        self.leisureFrame = Frame(self.possibleActivityFrame,bg='white',highlightthickness=2, highlightbackground="#00ccff")
        self.leisureFrame.place(relx=0.53,rely=0.15,relheight=0.6,relwidth=0.4)

        Label(self.leisureFrame, text="Ελεύθερου Χρόνου",font=('Times',20)).pack()

        self.scrollbarLeisure = Scrollbar(self.leisureFrame)
        self.scrollbarLeisure.pack(side=RIGHT,fill=Y)
        self.listboxLeisure = Listbox(self.leisureFrame,font=('TkHeading',15),yscrollcommand=self.scrollbarLeisure.set)
        self.listboxLeisure.pack(side=LEFT, fill=BOTH, expand=1)


        # Convert into list objects
        for i in range(len(lei)):
            lei[i] = list(lei[i])

        for i in range(len(com)):
            com[i] = list(com[i])

        # Rearrange leisure activities
        for i in range(len(lei)):
            for j in range(len(lei)-i-1):
                if lei[j][3] < lei[j+1][3]:
                    temp = lei[j+1]
                    lei[j+1] = lei[j]
                    lei[j] = temp


        # Rearrange commitment activities
        for i in range(len(com)):
            for j in range(len(com)-i-1):
                if com[j][3] < com[j+1][3]:
                    temp = com[j+1]
                    com[j+1] = com[j]
                    com[j] = temp


        for index in range(len(lei)):
            # String that contains the activity names
            if len(lei) != 0:
                if lei[index][4] <= self.graphData[4]:
                    self.leiGraph.append(lei[index])
                    self.displayStr = ''
                    self.displayStr = "{}. {}".format(index+1,lei[index][1])
                    self.listboxLeisure.insert(END, self.displayStr)


        for index in range(len(com)):
            # String that contains the activity names
            if len(com) != 0:
                if com[index][4] <= self.graphData[4]:
                    self.comGraph.append(com[index])
                    self.displayStr = ''
                    self.displayStr = "{}. {}".format(index+1,com[index][1])
                    self.listboxCommitment.insert(END, self.displayStr)





    # Checking if the graphData variable is empty(No user was selected)
    def activityProceedCheck(self):

        if not self.graphData:
            return
        else:
            # Resetting Label's content
            for i in range(4,8):
                self.userLabels[i]['text'] = ''

            self.fetchingData(3)


    # Returning back to the homepage
    def returnHomeFromUsers(self,check=0):

        if not check:
            self.registeredUsersFrame.destroy()
        else:
            self.possibleActivityFrame.destroy()
        self.mainMenu()



####### This function below can be called from different functions #######
                            # The default value is for the delete option
    def fetchingData(self,insertedList=0):


        # Proceed to choose an activity
        if insertedList == 3:

            # Resetting
            self.chosenActivity = None
            self.activityCategory = None
            self.leisureActivityData.clear()
            self.commitmentActivityData.clear()

            self.databaseButton['state'] = DISABLED
            self.possibleActivityButton['state'] = DISABLED
            self.homeButton['state'] = DISABLED
            self.activityRegisteredButton['state'] = DISABLED

            self.dropdownWindow = Toplevel(self.registeredUsersFrame)
            self.dropdownWindow.geometry("{}x{}+{}+{}".format(300, 250, self.registeredUsersFrame.winfo_x() + 900,self.registeredUsersFrame.winfo_y() + 300))


        # We triggered the function from the modify menu "Καταχωρημένοι"
        elif insertedList == 1:

            self.resettingLabelsBg()

            self.leisureActivityData.clear()
            self.commitmentActivityData.clear()
            self.registeredUser.clear()

            self.temporaryDataList[0]['text'] = ''
            self.temporaryDataList[1]['text'] = ''
            self.temporaryDataList[2]['text'] = ''

            self.modifyRegisteredButton['state'] = DISABLED
            self.homeModifyButton['state'] = DISABLED
            self.storeModifyButton['state'] = DISABLED
            self.addModifyButton['state'] = DISABLED
            self.activityModifyButton['state'] = DISABLED
            self.deleteModifyButton['state'] = DISABLED

            self.dropdownWindow = Toplevel(self.modifyFrame)
            self.dropdownWindow.geometry("{}x{}+{}+{}".format(300, 250, self.modifyFrame.winfo_x() + 900,self.modifyFrame.winfo_y() + 300))

        # We called the function from the activity button
        elif insertedList == 2:
            self.modifyRegisteredButton['state'] = DISABLED
            self.homeModifyButton['state'] = DISABLED
            self.storeModifyButton['state'] = DISABLED
            self.addModifyButton['state'] = DISABLED
            self.activityModifyButton['state'] = DISABLED
            self.deleteModifyButton['state'] = DISABLED

            self.dropdownWindow = Toplevel(self.modifyFrame)
            self.dropdownWindow.geometry("{}x{}+{}+{}".format(300, 250, self.modifyFrame.winfo_x() + 900,self.modifyFrame.winfo_y() + 300))

        # If the insertedList is not empty that means we called the function from the registeredUsers
        elif insertedList != 0:

            # Resetting
            self.graphData = ''
            self.leisureActivityData.clear()
            self.commitmentActivityData.clear()

            for num in range(12):
                self.userLabels[num]['text'] = ''


            # Disable the current buttons
            self.databaseButton['state'] = DISABLED
            self.possibleActivityButton['state'] = DISABLED
            self.homeButton['state'] = DISABLED
            self.activityRegisteredButton['state'] = DISABLED

            # Creating a window ontop of the current one
            self.dropdownWindow = Toplevel(self.registeredUsersFrame)
            self.dropdownWindow.geometry("{}x{}+{}+{}".format(300, 250, self.registeredUsersFrame.winfo_x() + 900,self.registeredUsersFrame.winfo_y() + 300))

        else: # The user triggered the function from the homepage's button "Διαγραφή"
            self.insertButton['state'] = DISABLED
            self.modifyButton['state'] = DISABLED
            self.deleteButton['state'] = DISABLED
            self.registerButton['state'] = DISABLED
            self.dropdownWindow = Toplevel(self.introFrame)
            self.dropdownWindow.geometry("{}x{}+{}+{}".format(300, 250, self.introFrame.winfo_x() + 700, self.introFrame.winfo_y() + 300))

        # We store the data from the database in a list of tuples(every tuple's a row/record)
        self.rows = self.readData()

        self.dropdownWindow.title("Registered Users")

        self.dropdownWindow.iconphoto(False,self.dataLogo)

        if insertedList==1 or insertedList==2:

            # Resetting
            self.newActivityData.clear()
            self.chosenActivity = None
            if insertedList == 2:
                self.clearModifyList(2)
            else:
                self.clearModifyList()

            self.categoryModify.set('-')

            def onClose():
                self.dropdownWindow.destroy()
                self.modifyRegisteredButton['state'] = NORMAL
                self.homeModifyButton['state'] = NORMAL
                self.storeModifyButton['state'] = NORMAL
                self.addModifyButton['state'] = NORMAL
                self.activityModifyButton['state'] = NORMAL
                self.deleteModifyButton['state'] = NORMAL

        elif insertedList != 0:
            # Bind a function to the WM_DELETE_WINDOW event of the window
            def onClose():
                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.possibleActivityButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL
                self.activityRegisteredButton['state'] = NORMAL

        else: # The user triggered the function from the homepage's button "Διαγραφή"
            def onClose():
                self.dropdownWindow.destroy()
                self.insertButton['state'] = NORMAL
                self.modifyButton['state'] = NORMAL
                self.deleteButton['state'] = NORMAL
                self.registerButton['state'] = NORMAL

        self.dropdownWindow.protocol("WM_DELETE_WINDOW",onClose)

        # Creating a scrollbar to navigate
        self.scrollbar = Scrollbar(self.dropdownWindow)
        self.scrollbar.pack(side=RIGHT,fill=Y)

        # Creating a listbox instance so we can navigate through the rows (records) (Θέλει δοκιμή)

        self.listboxData = Listbox(self.dropdownWindow,yscrollcommand=self.scrollbar.set)

        if insertedList==2:

                self.dropdownWindow.title("Activities")
                # Check if it's not empty
                if not self.commitmentActivityData[0]:
                    pass
                else:

                    for index in range(len(self.commitmentActivityData[0])):

                        # String that contains the activity names
                        self.displayStr = ''
                        self.displayStr = "{}".format(self.commitmentActivityData[0][index][1])
                        self.listboxData.insert(END,self.displayStr)

                if not self.leisureActivityData[0]:
                    pass
                else:

                    for index in range(len(self.leisureActivityData[0])):

                        # String that contains the activity names
                        self.displayStr = ''
                        self.displayStr = "{}".format(self.leisureActivityData[0][index][1])
                        self.listboxData.insert(END,self.displayStr)

        elif insertedList == 3:


            self.dropdownWindow.title("Activities")

            # Fetching data from the database
            self.reg, self.lei, self.com = self.primaryKeyData(self.graphData[0])
            self.commitmentActivityData.append(self.com)
            self.leisureActivityData.append(self.lei)


            # Check if it's not empty
            if not self.commitmentActivityData[0]:
                pass
            else:

                for index in range(len(self.commitmentActivityData[0])):
                    # String that contains the activity names
                    self.displayStr = ''
                    self.displayStr = "{}".format(self.commitmentActivityData[0][index][1])
                    self.listboxData.insert(END, self.displayStr)

            if not self.leisureActivityData[0]:
                pass
            else:

                for index in range(len(self.leisureActivityData[0])):
                    # String that contains the activity names
                    self.displayStr = ''
                    self.displayStr = "{}".format(self.leisureActivityData[0][index][1])
                    self.listboxData.insert(END, self.displayStr)


        else:
            # Showing only the user names
            for index in range(len(self.rows)):
                # Creating a string containing id and username
                self.displayStr = ''
                self.displayStr = "{}. {}".format(self.rows[index][0],self.rows[index][1])
                self.listboxData.insert(END,self.displayStr)

        self.listboxData.pack(side=LEFT,fill=BOTH,expand=1)
        self.scrollbar.config(command=self.listboxData.yview)

        self.acceptButton = Button(self.listboxData,text="OK",font=('TkHeadingFont',10),cursor='hand2',bd=3,command=lambda :self.databaseSelect(insertedList))
        self.acceptButton.pack(side=BOTTOM)

    def databaseSelect(self,insertedList):


        # This is activated whenever the user attends to delete from database
        if not insertedList:
            try:
                # Getting the row index
                self.selection = self.listboxData.curselection()[0]
                # Getting the primary key of the selected row and storing it
                self.selection = int((self.listboxData.get(self.selection)).split('.')[0])
                # Calling the respectively database function and passing the primary key
                self.deleteData(self.selection)

                self.dropdownWindow.destroy()
                self.insertButton['state'] = NORMAL
                self.modifyButton['state'] = NORMAL
                self.deleteButton['state'] = NORMAL
                self.registerButton['state'] = NORMAL
            except:
                # In case user presses ok without choosing (Πετάει σφάλμα)
                self.dropdownWindow.destroy()
                self.insertButton['state'] = NORMAL
                self.modifyButton['state'] = NORMAL
                self.deleteButton['state'] = NORMAL
                self.registerButton['state'] = NORMAL

        elif insertedList == 2:

            self.chosenActivity = None
            self.activityCategory = None
            try:

                self.selection = self.listboxData.curselection()[0]
                self.selection = self.listboxData.get(self.selection)


                # Getting the activity's data
                for item in self.commitmentActivityData[0]:

                    if self.selection in item:
                        self.chosenActivity = item
                        # Flag for commitment activity
                        self.activityCategory = 1
                        break

                for item in self.leisureActivityData[0]:

                    if self.selection in item:
                        self.chosenActivity = item
                        # Flag for leisure activity
                        self.activityCategory = 0
                        break


                self.categoryModify.set(self.chosenActivity[2])
                self.temporaryDataList[4].insert(0, self.chosenActivity[1])
                self.temporaryDataList[6].insert(0, self.chosenActivity[3])
                self.temporaryDataList[7].insert(0, self.chosenActivity[4])

                self.dropdownWindow.destroy()
                self.modifyRegisteredButton['state'] = NORMAL
                self.homeModifyButton['state'] = NORMAL
                self.storeModifyButton['state'] = NORMAL
                self.addModifyButton['state'] = NORMAL
                self.activityModifyButton['state'] = NORMAL
                self.deleteModifyButton['state'] = NORMAL
            except:
                self.dropdownWindow.destroy()
                self.modifyRegisteredButton['state'] = NORMAL
                self.homeModifyButton['state'] = NORMAL
                self.storeModifyButton['state'] = NORMAL
                self.addModifyButton['state'] = NORMAL
                self.activityModifyButton['state'] = NORMAL
                self.deleteModifyButton['state'] = NORMAL

        elif insertedList == 1:

            try:

                self.selection = self.listboxData.curselection()[0]
                # Primary key
                self.selection = int(self.listboxData.get(self.selection)[0])


                # Getting all the data from database for the activities

                self.reg,self.lei,self.com = self.primaryKeyData(self.selection)

                self.registeredUser.append(self.reg)
                self.commitmentActivityData.append(self.com)
                self.leisureActivityData.append(self.lei)

                self.temporaryDataList[0]['text'] = self.reg[1]
                self.temporaryDataList[1]['text'] = self.reg[2]
                self.temporaryDataList[2]['text'] = self.reg[3]
                self.temporaryDataList[3]['text'] = self.reg[4]


                self.dropdownWindow.destroy()
                self.modifyRegisteredButton['state'] = NORMAL
                self.homeModifyButton['state'] = NORMAL
                self.storeModifyButton['state'] = NORMAL
                self.activityModifyButton['state'] = NORMAL
                self.addModifyButton['state'] = NORMAL
                self.deleteModifyButton['state'] = NORMAL

            except:
                self.dropdownWindow.destroy()
                self.modifyRegisteredButton['state'] = NORMAL
                self.homeModifyButton['state'] = NORMAL
                self.storeModifyButton['state'] = NORMAL
                self.activityModifyButton['state'] = NORMAL
                self.addModifyButton['state'] = NORMAL
                self.deleteModifyButton['state'] = NORMAL

        elif insertedList == 3:

            try:

                self.selection = self.listboxData.curselection()[0]
                self.selection = self.listboxData.get(self.selection)

                # Getting the activity's data
                for item in self.commitmentActivityData[0]:

                    if self.selection in item:
                        self.chosenActivity = item
                        # Flag for commitment activity
                        self.activityCategory = 1
                        break

                for item in self.leisureActivityData[0]:

                    if self.selection in item:

                        self.chosenActivity = item
                        # Flag for leisure activity
                        self.activityCategory = 0

                        break



                self.userLabels[4]['text'] = self.chosenActivity[1]
                self.userLabels[5]['text'] = self.chosenActivity[2]
                self.userLabels[6]['text'] = self.chosenActivity[3]
                self.userLabels[7]['text'] = self.chosenActivity[4]



                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.possibleActivityButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL
                self.activityRegisteredButton['state'] = NORMAL
            except:
                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.possibleActivityButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL
                self.activityRegisteredButton['state'] = NORMAL



        else:
            # Getting the index of the chosen row
            try:
                self.selection = self.listboxData.curselection()[0]
                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.possibleActivityButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL
                self.activityRegisteredButton['state'] = NORMAL

                for num in range(4):
                    self.userLabels[num]['text'] = self.rows[self.selection][num + 1]

                # We store the chosen row, including primary key
                self.graphData = self.rows[self.selection]

                # Calculating activity stats (Εδώ για τα γραφήματα)
                meanCommitment,meanLeisure,timeCommitment,timeLeisure = self.calculateData(self.graphData[0])

                self.userLabels[11]['text'] = meanCommitment
                self.userLabels[10]['text'] = meanLeisure
                self.userLabels[9]['text'] = timeCommitment
                self.userLabels[8]['text'] = timeLeisure

            except:
                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.possibleActivityButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL
                self.activityRegisteredButton['state'] = NORMAL

## Delete a particular activity ##
    def deleteParticularActivity(self):
        if not self.registeredUser or self.chosenActivity == None:
            return

        # Proceed in deleting the choosen activity
        self.deleteSpecificActivity(self.activityCategory,self.chosenActivity[0],self.chosenActivity[1])

        # Refresh the current menu
        self.fetchingData(1)


#### Delete from database ####
    # When the user wants to delete a registered user from the database
    def delete(self):
        self.fetchingData()


    def addNewActivity(self):
        self.chosenActivity = None
        self.newActivityData.clear()
        if not self.registeredUser:
            return
        else:
            self.insertContinue(self.registeredUser[0][0], 1)


    def clearModifyList(self,check=0):
        self.categoryModify.set('-')
        if not check:
            self.temporaryDataList[3]['text'] = ''

        self.temporaryDataList[4].delete(0, 'end')
        self.temporaryDataList[6].delete(0, 'end')
        self.temporaryDataList[7].delete(0, 'end')

    ### Creating a dropdown menu ###
    def chooseActivity(self):
        if not self.registeredUser:
            return
        else:
            self.resettingLabelsBg()
            self.fetchingData(2)

    def backFromModify(self):
        self.chosenActivity = None
        self.modifyFrame.destroy()
        self.mainMenu()

    def resettingLabelsBg(self):
        for index in range(4, 8):
            self.temporaryDataList[index]['bg'] = 'white'


## Building the store functionality ##

    def storeModifyActivity(self,category):

        if self.chosenActivity is None:
            return

        else:
            # 1 stands for commitment activities, 0 for leisure
            # Passing category (1 or 0) and activity's name
            self.resettingLabelsBg()
            self.newActivityData.clear()
            for index in range(4,8):
                if index != 5:
                    self.newActivityData.append(self.temporaryDataList[index].get())
                else:
                    self.newActivityData.append(self.categoryModify.get())

            # Checking if values are valid

            if self.newActivityData[0] == '':
                self.temporaryDataList[4]['bg'] = 'red'
                return
            try:
                if int(self.newActivityData[2])>0 and int(self.newActivityData[2])<11:
                    pass
                else:
                    raise Exception
            except:
                self.temporaryDataList[6]['bg'] = 'red'
                return
            try:
                if int(self.newActivityData[3])>-1 and int(self.newActivityData[3])<169:
                    pass
                else:
                    raise Exception
            except:
                self.temporaryDataList[7]['bg'] = 'red'
                return


            if category == 0:
                if self.newActivityData[1] == "Ελεύθερου Χρόνου":
                    # Then we will update the database
                    self.updateDatabase(category,self.chosenActivity[0],self.chosenActivity[1],*self.newActivityData)

                # Else delete from leisure table the activity and add it to the commitment table
                else:
                    self.changeActivity(category,self.chosenActivity[0],self.chosenActivity[1],*self.newActivityData)

            else:
                if self.newActivityData[1] == "Υποχρεώσεων":
                    # Then we will update the database
                    self.updateDatabase(category,self.chosenActivity[0],self.chosenActivity[1],*self.newActivityData)

                # Else delete from commitment table the activity and add it to the leisure table
                else:
                    self.changeActivity(category,self.chosenActivity[0],self.chosenActivity[1],*self.newActivityData)

            # Refresh the current menu
            self.fetchingData(1)



########## This section below is for the modify menu ##########
    def modify(self):

        # Resetting
        self.introFrame.destroy()
        self.categoryModify = StringVar(value='-')
        self.newActivityData.clear()
        self.leisureActivityData.clear()
        self.commitmentActivityData.clear()
        self.registeredUser.clear()
        self.temporaryDataList.clear()

        # Modify frame initialized
        self.modifyFrame = Frame(self.entryWindow,width=WIDTH,height=HEIGHT,bg=basicColor)
        self.modifyFrame.pack()

        self.position = 0.03
        self.labelModifyActivities=['Ονοματεπώνυμο','Φύλο','Ηλικία','Διαθέσιμες ώρες ανά Εβδομάδα','Δραστηριότητα','Κατηγορία','Βαθμός Σημαντικότητας','Διάρκεια ανά Εβδομάδα(ώρες)']

        for data in self.labelModifyActivities:
            Label(self.modifyFrame,relief="groove",borderwidth=2,bg="#99ccff",font=('TkHeadingFont', 20),text=data).place(relx=0.04,rely=self.position,relwidth=0.31,relheight=0.08)
            self.position += 0.12

        self.position = 0.03
        for num in range(8):
            if num < 4:
                self.temporaryDataList.append(Label(self.modifyFrame,font=('TkHeadingFont', 20)))
                self.temporaryDataList[num].place(relx=0.4, rely=self.position, relwidth=0.31, relheight=0.08)
            elif num == 5:
                # Dropdown Menu for the category (in modify)
                self.temporaryDataList.append(OptionMenu(self.modifyFrame, self.categoryModify, "Υποχρεώσεων", "Ελεύθερου Χρόνου"))
                self.temporaryDataList[num]['font'] = ('Times', 15)
                self.temporaryDataList[num].config(indicatoron=False)
                self.temporaryDataList[num].config(activebackground='light blue')
                self.temporaryDataList[num]['cursor'] = "hand2"
                self.temporaryDataList[num].place(relx=0.4, rely=self.position, relwidth=0.31, relheight=0.08)
            else:
                self.temporaryDataList.append(Entry(self.modifyFrame, font=('TkHeadingFont', 15)))
                self.temporaryDataList[num].place(relx=0.4, rely=self.position, relwidth=0.31, relheight=0.08)

            self.position += 0.12

        # Getting all data from a specific registered user
        self.modifyRegisteredButton = Button(self.modifyFrame,font=('TkHeadingFont',15),cursor='hand2',text="Καταχωρημένοι",bd=3,command=lambda :self.fetchingData(1))
        self.modifyRegisteredButton.place(relx=0.80,rely=0.05,relwidth=0.15,relheight=0.1)

        self.homeModifyButton = Button(self.modifyFrame,font=('TkHeadingFont',15),cursor='hand2',text="Αρχική",bd=3,command=self.backFromModify)
        self.homeModifyButton.place(relx=0.80,rely=0.80,relwidth=0.15,relheight=0.1)

        self.storeModifyButton = Button(self.modifyFrame,font=('TkHeadingFont',15),cursor='hand2',text="Αποθήκευση",bd=3,command=lambda :self.storeModifyActivity(self.activityCategory))
        self.storeModifyButton.place(relx=0.80,rely=0.35,relwidth=0.15,relheight=0.1)

        self.activityModifyButton = Button(self.modifyFrame,font=('TkHeadingFont',15),cursor='hand2',text="Δραστηριότητα",bd=3,command=self.chooseActivity)
        self.activityModifyButton.place(relx=0.80,rely=0.2,relwidth=0.15,relheight=0.1)

        self.addModifyButton = Button(self.modifyFrame,font=('TkHeadingFont',15),cursor='hand2',text="Προσθήκη",bd=3,command=self.addNewActivity)
        self.addModifyButton.place(relx=0.80,rely=0.65,relwidth=0.15,relheight=0.1)

        self.deleteModifyButton = Button(self.modifyFrame,font=('TkHeadingFont',15),cursor='hand2',text="Διαγραφή",bd=3,command=self.deleteParticularActivity)
        self.deleteModifyButton.place(relx=0.80,rely=0.50,relwidth=0.15,relheight=0.1)


########## This Block here is for inserting a new user ##########

    def insert(self):

        # Resetting
        self.temporaryDataList.clear()

        self.introFrame.destroy()

        # insert frame initialized
        self.modifyBase = Frame(self.entryWindow, width=WIDTH, height=HEIGHT, bg=basicColor)
        self.modifyBase.pack()

        # Buttons attached to the insert window
        self.newUserLabel = Label(self.modifyBase,relief="groove",borderwidth=2,text="Εισαγωγή Νέου Χρήστη",font=('Times',20),bg="#99ccff")
        self.newUserLabel.place(relheight=0.1,relwidth=0.3,relx=0.35,rely=0.05)

        self.insertNameLabel = Label(self.modifyBase,bg="#99ccff",relief="groove",borderwidth=2,text="Ονοματεπώνυμο :",font=('Times',20))
        self.insertNameLabel.place(relheight=0.05,relwidth=0.2,relx=0.12,rely=0.35)

        self.insertNameEntry = Entry(self.modifyBase,font=('Times',15),bd=3)
        self.insertNameEntry.place(relheight=0.1,relwidth=0.2,relx=0.40,rely=0.32)

        self.sexLabel = Label(self.modifyBase,bg="#99ccff",relief="groove",borderwidth=2,text="Φύλο :",font=('Times',20))
        self.sexLabel.place(relheight=0.05,relwidth=0.1,relx=0.22,rely=0.50)

        self.sexCheck = StringVar(value="n")
        self.sexOptionMale = Checkbutton(self.modifyBase,relief="ridge",borderwidth=3,text="Άνδρας ",font=('Times',15),variable=self.sexCheck,onvalue="male",offvalue="n")
        self.sexOptionFemale = Checkbutton(self.modifyBase,relief="ridge",borderwidth=3,text="Γυναίκα ", font=('Times', 15), variable=self.sexCheck,onvalue="female",offvalue="n")
        self.sexOptionMale.deselect()
        self.sexOptionFemale.deselect()
        self.sexOptionMale.place(relx=0.40,rely=0.50)
        self.sexOptionFemale.place(relx=0.52, rely=0.50)

        self.userAge = Label(self.modifyBase,bg="#99ccff",relief="groove",borderwidth=2,text="Ηλικία :",font=('Times',20))
        self.userAge.place(relheight=0.05, relwidth=0.1, relx=0.22, rely=0.65)

        self.dropdownAge = Entry(self.modifyBase, font=('Times',15),bd=3)
        self.dropdownAge.place(relheight=0.05, relwidth=0.1, relx=0.45, rely=0.65)

        self.activityDurationLabel = Label(self.modifyBase,bg="#99ccff",relief="groove",borderwidth=2,text="Συνολικός Χρόνος :",font=('Times',20))
        self.activityDurationLabel.place(relheight=0.05, relwidth=0.24, relx=0.08, rely=0.80)
        self.activityDuration = Entry(self.modifyBase, font=('Times',15),bd=3)
        self.activityDuration.place(relheight=0.05,relwidth=0.1,relx=0.45,rely=0.80)


        # The continue button that moves the control to the checkFirstPage method
        self.insertContinueButton = Button(self.modifyBase,image=self.right,cursor="hand2",command=self.checkFirstPage)
        self.insertContinueButton.place(relheight=0.09, relwidth=0.05, relx=0.90, rely=0.5)

        self.insertBackButton = Button(self.modifyBase,image=self.left,cursor="hand2",command=self.insertBack)
        self.insertBackButton.place(relheight=0.09, relwidth=0.05, relx=0.05, rely=0.5)


    # Check if the user filled correctly the first three fields
    require1=0 # This class attribute is used as a flag
    def checkFirstPage(self):

        self.dropdownAge['bg'] = 'white'
        self.activityDuration['bg'] = 'white'
        # The code below creates one label at a time so we don't have issues when deleting it
        if not self.require1:
            self.starFirst = Label(self.modifyBase,text="*(Required)",bg=basicColor,fg='#ff3300',font=("Times",20))
            # Set the require1 to 1 so no more label instances are created (Όταν επιχειρεί ο χρήστης να συνεχίσει)
            self.require1+=1

        # Getting the data from the entry instance
        self.checkField = self.insertNameEntry.get()

        # The code below does some sort of defensive programming
        if not self.checkField:
            self.starFirst.place(relx=0.61,rely=0.33)
        else:
            self.checkField = self.dropdownAge.get()
            if not self.checkField:
                self.starFirst.place(relx=0.56,rely=0.65)
            else:
                try:
                    int(self.checkField)
                    if int(self.checkField) <1 or int(self.checkField)>100:
                        raise Exception
                except:
                        self.dropdownAge['bg']='#ff471a'
                        self.starFirst.place(relx=0.56, rely=0.65)
                        return


                self.checkField =  self.activityDuration.get()

                if not self.checkField:
                    self.starFirst.place(relx=0.56,rely=0.80)
                    return
                else:
                    try:
                        int(self.checkField)
                        if int(self.checkField) < 0 or int(self.checkField) > 168:
                            raise Exception

                    except:
                            self.activityDuration['bg'] = '#ff471a'
                            self.starFirst.place(relx=0.56,rely=0.80)
                            return


                if self.sexCheck.get() == "n":
                    self.starFirst.place(relx=0.61,rely=0.50)
                else:
                    self.require1=0

                    # Adding the first 4 fields to the class list
                    self.temporaryDataList.append(self.insertNameEntry.get())
                    self.temporaryDataList.append(self.sexCheck.get())
                    self.temporaryDataList.append(int(self.dropdownAge.get()))
                    self.temporaryDataList.append(int(self.activityDuration.get()))

                    # Also adding the data to the registers table
                    self.addUser(*self.temporaryDataList)

                    # Getting and storing the id of the inserted user, passing it into the insertContinue function below afterwards
                    self.primaryKey = self.cur.lastrowid

                    self.starFirst.destroy()
                    self.insertContinue(self.primaryKey)


    # The change between the frames
    def insertBack(self):
        # Destroy the starFirst label
        if self.require1==1:
            self.starFirst.destroy()
            self.require1=0

        self.modifyBase.destroy()
        self.mainMenu()



    # After successfully added the user we proceed to the activities section, keeping track of the primary key of course
    def insertContinue(self,user_id,check=0):

        if not check:
            self.modifyBase.destroy()
        else:
            self.modifyFrame.destroy()

        # Create the base for all the widgets
        self.continueInsertFrame = Frame(self.entryWindow, width=WIDTH, height=HEIGHT, bg=basicColor)
        self.continueInsertFrame.pack()

        self.dataLabel = Label(self.continueInsertFrame,relief="groove",borderwidth=2,text="Παρακαλώ συμπληρώστε τα στοιχεία σε όλα τα πεδία\n\n   Δεδομένα",font=('TkHeadingFont',20),bg="#99ccff")
        self.dataLabel.place(relheight=0.15, relwidth=0.60, relx=0.20, rely=0.01)

        # Name of the activity
        self.nameActivityLabel = Label(self.continueInsertFrame,relief="groove",borderwidth=2,text="Όνομα\nΔραστηριότητας",font=('TkHeadingFont',20),bg="#99ccff")
        self.nameActivityLabel.place(relx=0.2,rely=0.27)

        # Category of the activity
        self.activityLabel = Label(self.continueInsertFrame,relief="groove",borderwidth=2,text="Κατηγορία\nΔραστηριότητας",font=('Times',20),bg="#99ccff")
        self.activityLabel.place(relx=0.1,rely=0.5)
        self.activityName = Entry(self.continueInsertFrame,relief="ridge",borderwidth=3,font=('Times',15))
        self.activityName.place(relheight=0.1,relwidth=0.2,relx=0.4, rely=0.27)

        # Dropdown Menu for the category
        self.category = StringVar(value='-')
        self.activityDropDown = OptionMenu(self.continueInsertFrame,self.category,"Υποχρεώσεων","Ελεύθερου Χρόνου")
        self.activityDropDown['font'] = ('Times',15)
        self.activityDropDown['cursor'] = "hand2"
        self.activityDropDown.config(indicatoron=False)
        self.activityDropDown.config(activebackground='light blue')
        self.activityDropDown.place(relx=0.1,rely=0.7,relwidth=0.15, relheight=0.07)

        # Significant rate
        self.significantLabel = Label(self.continueInsertFrame,relief="groove",borderwidth=2,text="Βαθμός\nΣημαντικότητας",font=('Times',20),bg="#99ccff")
        self.significantLabel.place(relx=0.70,rely=0.5)
        self.significantScale = Scale(self.continueInsertFrame,relief="ridge",borderwidth=3,from_=1,to=10,orient=HORIZONTAL)
        self.significantScale.place(relx=0.73,rely=0.7)

        # Week duration in hours
        self.weekDuration = Label(self.continueInsertFrame,relief="groove",borderwidth=2,text="Εβδομαδιαία\nΔιάρκεια(ώρες)",font=('Times',20),bg="#99ccff")
        self.weekDuration.place(relx=0.43,rely=0.5)
        self.durationSpinbox = Spinbox(self.continueInsertFrame,relief="ridge",borderwidth=3,from_=0,to=168,font=('Times',15),validate='all',validatecommand=(self.entryWindow.register(self.spinboxCheck), '%P'))
        self.durationSpinbox.place(relx=0.46,rely=0.7,width=100,height=50)

        # Cancel Button
        self.cancelButton = Button(self.continueInsertFrame,font=('TkHeadingFont',15),cursor="hand2",text="Αρχική",bd=3,command=self.cancel)
        self.cancelButton.place(relx=0.10, rely=0.85)

        # Add Button
        self.addButton = Button(self.continueInsertFrame,font=('TkHeadingFont',15),cursor="hand2",text="Προσθήκη",bd=3,command=lambda :self.checkSecondPage(user_id))
        self.addButton.place(relx=0.80, rely=0.85)

    def cancel(self):
        # Destroy the starSecond label
        if self.require2==1:
            self.starSecond.destroy()
            self.require2=0
        self.continueInsertFrame.destroy()
        self.mainMenu()

    # After passing successfully the first three fields we end up with the last ones
    require2 = 0 # This also for flag using
    def checkSecondPage(self,user_id):

        if not self.require2:
            self.starSecond = Label(self.continueInsertFrame, text="*(Required)", bg=basicColor, fg='#ff3300', font=("Times", 20))
            # Set the require2 to 1 so no more label instances are created (Το ίδιο σαν το προηγούμενο label)
            self.require2 += 1

        # Getting the data from the entry instance
        self.checkSecondField = self.activityName.get()

        if not self.checkSecondField:
            self.starSecond.place(relx=0.60, rely=0.28)
        else:
            self.checkSecondField = self.category.get()
            if self.checkSecondField == '-':
                self.starSecond.place(relx=0.25,rely=0.7)
            else:
                self.require2=0
                self.temporaryDataList.clear()
                # Adding the last fields to the class
                self.temporaryDataList.append(self.activityName.get())
                self.temporaryDataList.append(self.category.get())
                self.temporaryDataList.append(int(self.significantScale.get()))
                self.temporaryDataList.append(int(self.durationSpinbox.get()))


                # Final step is adding to the database depending of the activity category
                if self.temporaryDataList[1] == "Υποχρεώσεων":
                    self.addCommitmentActivity(user_id, *(self.temporaryDataList))
                else:
                    self.addLeisureActivity(user_id, *(self.temporaryDataList))

                self.starSecond.destroy()
                self.addFinished()

    def addFinished(self):

        # After successfully adding the data, we reset everything
        self.temporaryDataList.clear()
        self.category.set(value='-')
        self.activityName.delete(0,'end')
        self.significantScale.set(0)
        self.durationSpinbox.delete(0,'end')
        self.durationSpinbox.insert(0,0)

    # A function that checks the range of the spinboxes (Αμυντικός προγραμματισμός)
    def spinboxCheck(self,text):
        if text:
            try:
                value = int(text)
                if value < 0 or value > 168:
                    return False
            except ValueError:
                return False
        return True


if __name__ == "__main__":
    app = app()
    # The mainloop command
    app.entryWindow.mainloop()