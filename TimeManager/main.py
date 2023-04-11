from tkinter import *
from PIL import Image,ImageTk
import sqlite3
from database import Database

WIDTH = 1280
HEIGHT = 720

# This is used for rescaling the background image
IMAGESIZE = (WIDTH,HEIGHT)

# Starting menu
class introMenu(Database):

    # With this variable we keep track of the primary key
    primaryKey = 0

    # Temporary class list for the database
    temporaryData = []

    # Temporary variable for the graphs
    graphVariable = ''

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

        # Favicon image
        self.entryWindow.iconphoto(False, self.favicon)


        # Initializing
        self.introFunctionFrame()

        # The mainloop command
        self.entryWindow.mainloop()

    def introFunctionFrame(self):

        # Creating the main frame widget into self.entryWindow
        self.introFrame = Frame(self.entryWindow,width=WIDTH,height=HEIGHT,bg="#009999")
        self.introFrame.pack()

        # Putting an image into the frame
        self.backgroundImage = Label(self.introFrame,image=self.background)
        self.backgroundImage.place(x=0,y=0,relheight=1,relwidth=1)

        # Putting a label
        Label(self.backgroundImage,text="Καλώς Ήρθατε!",font=('TkHeadingFont', 25)).place(relx=0.4,rely=0.2)

        #Buttons attached to the intro window (ontop of the image)
        self.insertButton = Button(self.backgroundImage,font=('TkHeadingFont',15),cursor="hand2", text="Εισαγωγή",bd=3, command=self.insert)
        self.insertButton.place(relx=0.62,rely=0.8)

        self.modifyButton = Button(self.backgroundImage,font=('TkHeadingFont',15),cursor="hand2", text="Τροποποίηση",bd=3, command=self.modify)
        self.modifyButton.place(relx=0.44,rely=0.8)

        self.deleteButton = Button(self.backgroundImage,font=('TkHeadingFont',15),cursor="hand2", text="Διαγραφή",bd=3, command=self.delete)
        self.deleteButton.place(relx=0.28,rely=0.8)

        self.registerButton = Button(self.backgroundImage,font=('TkHeadingFont',30),cursor="hand2", text="Χρήστες",padx=15,bd=3,image=self.userLogo,compound="left", command=self.registeredUsers)
        self.registerButton.place(relx=0.39,rely=0.4,relheight=0.2,relwidth=0.2)

    # Getting Access to the database
    def registeredUsers(self):

        # Destroying the previous frame
        self.introFrame.destroy()

        # This variable will be used for the graphing part
        self.graphVariable = ''

        # The list below keeps track of the entries
        self.entryList = []

        # RegisteredUsers frame initialized
        self.registeredUsersFrame = Frame(self.entryWindow,width=WIDTH,height=HEIGHT,bg="#99ccff")
        self.registeredUsersFrame.pack()

        # Variable for positioning labels
        self.position = 0.03
        self.labelDataUsers=['Ονοματεπώνυμο','Φύλο','Ηλικία','Δραστηριότητα','Κατηγορία','Βαθμός Σημαντικότητας','Διάρκεια ανά Εβδομάδα(ώρες)','Διαθέσιμες ώρες ανά Εβδομάδα']

        for data in self.labelDataUsers:
            Label(self.registeredUsersFrame,font=('TkHeadingFont', 20),text=data).place(relx=0.04,rely=self.position,relwidth=0.31,relheight=0.08)
            self.position += 0.12

        self.position = 0.03
        for num in range(8):
            self.entryList.append(Label(self.registeredUsersFrame,font=('TkHeadingFont', 15)))
            self.entryList[num].place(relx=0.4,rely=self.position,relwidth=0.31,relheight=0.08)
            self.position += 0.12

        # Button that fetches data from the database file
        self.databaseButton = Button(self.registeredUsersFrame,font=('TkHeadingFont',15),cursor='hand2',text="Καταχωρημένοι",bd=3,command=lambda :self.fetchingData(self.entryList))
        self.databaseButton.place(relx=0.80,rely=0.1,relwidth=0.15,relheight=0.1)

        # Button that goes to the graph section
        self.graphButton = Button(self.registeredUsersFrame,font=('TkHeadingFont',15),cursor='hand2',text="Γράφημα",bd=3)
        self.graphButton.place(relx=0.80,rely=0.45,relwidth=0.15,relheight=0.1)

        # Button that returns to the homepage
        self.homeButton = Button(self.registeredUsersFrame,font=('TkHeadingFont',15),cursor='hand2',text="Αρχική",bd=3,command=self.returnHomeFromData)
        self.homeButton.place(relx=0.80,rely=0.8,relwidth=0.15,relheight=0.1)

    # Returning back the homepage
    def returnHomeFromData(self):

        self.registeredUsersFrame.destroy()
        self.introFunctionFrame()

    def fetchingData(self,insertedList=0):

        # If the insertedList is not empty that means we called the function from the registeredUsers
        if insertedList != 0:
            # Disable the current buttons
            self.databaseButton['state'] = DISABLED
            self.graphButton['state'] = DISABLED
            self.homeButton['state'] = DISABLED

            # Creating a window ontop of the current one
            self.dropdownWindow = Toplevel(self.registeredUsersFrame)
            self.dropdownWindow.geometry("{}x{}+{}+{}".format(300, 250, self.registeredUsersFrame.winfo_x() + 900,self.registeredUsersFrame.winfo_y() + 300))
        else:
            self.insertButton['state'] = DISABLED
            self.modifyButton['state'] = DISABLED
            self.deleteButton['state'] = DISABLED
            self.registerButton['state'] = DISABLED
            self.dropdownWindow = Toplevel(self.introFrame)
            self.dropdownWindow.geometry("{}x{}+{}+{}".format(300, 250, self.introFrame.winfo_x() + 700, self.introFrame.winfo_y() + 300))

        # We store the data from the database in a list of tuples(every tuple's a row)
        self.rows = self.readData()

        self.dropdownWindow.title("Registered Users")

        self.dropdownWindow.iconphoto(False,self.dataLogo)

        if insertedList != 0:
            # Bind a function to the WM_DELETE_WINDOW event of the window
            def onClose():
                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.graphButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL

            self.dropdownWindow.protocol("WM_DELETE_WINDOW", onClose)
        else:
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

        # Creating a listbox instance so we can navigate through the rows
        self.listboxData = Listbox(self.dropdownWindow,yscrollcommand=self.scrollbar.set)


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
                self.selection = int(self.listboxData.get(self.selection)[0])

                # Calling the respectively database function and passing the primary key
                self.deleteData(self.selection)

                self.dropdownWindow.destroy()
                self.insertButton['state'] = NORMAL
                self.modifyButton['state'] = NORMAL
                self.deleteButton['state'] = NORMAL
                self.registerButton['state'] = NORMAL
            except:
                self.dropdownWindow.destroy()
                self.insertButton['state'] = NORMAL
                self.modifyButton['state'] = NORMAL
                self.deleteButton['state'] = NORMAL
                self.registerButton['state'] = NORMAL
        else:
            # Getting the index of the chosen row
            try:
                self.selection = self.listboxData.curselection()[0]
                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.graphButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL

                for num in range(8):
                    insertedList[num]['text'] = self.rows[self.selection][num]

                # We store the chosen row
                self.graphVariable = self.rows[self.selection]
            except:
                self.dropdownWindow.destroy()
                self.databaseButton['state'] = NORMAL
                self.graphButton['state'] = NORMAL
                self.homeButton['state'] = NORMAL

    def delete(self):
        self.fetchingData()

    def modify(self):
        self.introFrame.destroy()

        #modify frame initialized
        self.modifyFrame = Frame(self.entryWindow,width=WIDTH,height=HEIGHT,bg="#99ccff")
        self.modifyFrame.pack()


########## This Block here is for inserting new data ##########
    def insert(self):

        # Resetting the class list
        self.temporaryData = []

        self.introFrame.destroy()

        # insert frame initialized
        self.modifyBase = Frame(self.entryWindow, width=WIDTH, height=HEIGHT, bg="#99ccff")
        self.modifyBase.pack()

        # Buttons attached to the insert window
        self.newUserLabel = Label(self.modifyBase,text="Εισαγωγή Νέου Χρήστη",font=('Times',20),bg="white")
        self.newUserLabel.place(relheight=0.1,relwidth=0.3,relx=0.35,rely=0.20)

        self.insertNameLabel = Label(self.modifyBase,text="Ονοματεπώνυμο :",font=('Times',20),bg="white")
        self.insertNameLabel.place(relheight=0.05,relwidth=0.2,relx=0.12,rely=0.5)

        self.insertNameEntry = Entry(self.modifyBase,font=('Times',15),bd=3)
        self.insertNameEntry.place(relheight=0.1,relwidth=0.2,relx=0.40,rely=0.47)

        self.sexLabel = Label(self.modifyBase,text="Φύλο :",font=('Times',20),bg="white")
        self.sexLabel.place(relheight=0.05,relwidth=0.1,relx=0.22,rely=0.65)

        self.sexCheck = StringVar(value="n")
        self.sexOptionMale = Checkbutton(self.modifyBase,text="Άνδρας ",font=('Times',15),variable=self.sexCheck,onvalue="male",offvalue="n")
        self.sexOptionFemale = Checkbutton(self.modifyBase, text="Γυναίκα ", font=('Times', 15), variable=self.sexCheck,onvalue="female",offvalue="n")
        self.sexOptionMale.deselect()
        self.sexOptionFemale.deselect()
        self.sexOptionMale.place(relx=0.40,rely=0.65)
        self.sexOptionFemale.place(relx=0.52, rely=0.65)

        self.userAge = Label(self.modifyBase,text="Ηλικία :",font=('Times',20),bg="white")
        self.userAge.place(relheight=0.05, relwidth=0.1, relx=0.22, rely=0.80)

        self.dropdownAge = Entry(self.modifyBase, font=('Times',15),bd=3)
        self.dropdownAge.place(relheight=0.05, relwidth=0.1, relx=0.45, rely=0.80)


        # The continue button that moves the control to the checkFirstPage method
        self.insertContinueButton = Button(self.modifyBase,image=self.right,cursor="hand2",command=self.checkFirstPage)
        self.insertContinueButton.place(relheight=0.09, relwidth=0.05, relx=0.90, rely=0.80)

        self.insertBackButton = Button(self.modifyBase,image=self.left,cursor="hand2",command=self.insertBack)
        self.insertBackButton.place(relheight=0.09, relwidth=0.05, relx=0.05, rely=0.80)


    # Check if the user filled correctly the first three fields
    require1=0 # This class attribute is used as a flag
    def checkFirstPage(self):

        self.dropdownAge['bg'] = 'white'

        # The code below creates one label at a time so we don't have issues when deleting it
        if not self.require1:
            self.starFirst = Label(self.modifyBase,text="*(Required)",bg="#99ccff",fg='red',font=("Times",25))
            # Set the require to 1 so no more label instances are created
            self.require1+=1

        # Getting the data from the entry instance
        self.checkField = self.insertNameEntry.get()

        # The code below does some sort of defensive programming
        if not self.checkField:
            self.starFirst.place(relx=0.61,rely=0.48)
        else:
            self.checkField = self.dropdownAge.get()
            if not self.checkField:
                self.starFirst.place(relx=0.56,rely=0.79)
            else:
                try:
                    int(self.checkField)
                    if int(self.checkField) <1 or int(self.checkField)>100:
                        raise Exception
                except:
                        self.dropdownAge['bg']='#ff471a'
                        self.starFirst.place(relx=0.56, rely=0.79)
                        return
                if self.sexCheck.get() == "n":
                    self.starFirst.place(relx=0.61,rely=0.64)
                else:
                    self.require1=0

                    self.temporaryData = []

                    # Adding the first 3 fields to the class list
                    self.temporaryData.append(self.insertNameEntry.get())
                    self.temporaryData.append(self.sexCheck.get())
                    self.temporaryData.append(int(self.dropdownAge.get()))

                    # Also adding the data to the registers table
                    self.addUser(*self.temporaryData)

                    # Getting and storing the id of the inserted user, passing it into the insertContinue function below afterwards
                    self.primaryKey = self.cur.lastrowid


                    self.starFirst.destroy()
                    self.insertContinue(self.primaryKey)


    # The change between the widgets
    def insertBack(self):
        # Destroy the starFirst label
        if self.require1==1:
            self.starFirst.destroy()
            self.require1=0

        self.modifyBase.destroy()
        self.introFunctionFrame()



    # After adding the user we proceed to the activities section, keeping track of the primary key of course
    def insertContinue(self,user_id):

        self.modifyBase.destroy()

        # Create the base for all the widgets
        self.continueInsertFrame = Frame(self.entryWindow, width=WIDTH, height=HEIGHT, bg="#99ccff")
        self.continueInsertFrame.pack()

        self.dataLabel = Label(self.continueInsertFrame,text="Παρακαλώ συμπληρώστε τα στοιχεία σε όλα τα πεδία\n\n   Δεδομένα",font=('TkHeadingFont',20),bg="#99ccff")
        self.dataLabel.place(relheight=0.15, relwidth=0.60, relx=0.20, rely=0.01)

        # Name of the activity
        self.nameActivityLabel = Label(self.continueInsertFrame,text="Όνομα\nΔραστηριότητας",font=('TkHeadingFont',20),bg='white')
        self.nameActivityLabel.place(relx=0.2,rely=0.25)

        # Category of the activity
        self.activityLabel = Label(self.continueInsertFrame,text="Κατηγορία\nΔραστηριότητας",font=('Times',20),bg="white")
        self.activityLabel.place(relx=0.1,rely=0.5)
        self.activityName = Entry(self.continueInsertFrame, font=('Times',15),bd=3)
        self.activityName.place(relheight=0.1,relwidth=0.2,relx=0.4, rely=0.25)

        # Dropdown Menu for the category
        self.category = StringVar(value='-')
        self.activityDropDown = OptionMenu(self.continueInsertFrame,self.category,"Υποχρεώσεων","Ελεύθερου Χρόνου")
        self.activityDropDown['font'] = ('Times',15)
        self.activityDropDown['highlightbackground'] = "black"
        self.activityDropDown.place(relx=0.10,rely=0.7)

        # Significant rate
        self.significantLabel = Label(self.continueInsertFrame,text="Βαθμός\nΣημαντικότητας",font=('Times',20),bg="white")
        self.significantLabel.place(relx=0.50,rely=0.5)
        self.significantScale = Scale(self.continueInsertFrame,from_=1,to=10,orient=HORIZONTAL)
        self.significantScale.place(relx=0.53,rely=0.7)

        # Week duration in hours
        self.weekDuration = Label(self.continueInsertFrame,text="Εβδομαδιαία\nΔιάρκεια(ώρες)",font=('Times',20),bg="white")
        self.weekDuration.place(relx=0.3,rely=0.5)
        self.durationSpinbox = Spinbox(self.continueInsertFrame,from_=0,to=168,font=('Times',15),validate='all',validatecommand=(self.entryWindow.register(self.spinboxCheck), '%P'))
        self.durationSpinbox.place(relx=0.33,rely=0.7,width=100,height=30)

        # Available time per week
        self.availableTimeLabel = Label(self.continueInsertFrame,text="Διαθέσιμος\nΧρόνος\nανά Εβδομάδα(ώρες)",font=('Times',20),bg="white")
        self.availableTimeLabel.place(relx=0.7,rely=0.46)
        self.availableSpinbox = Spinbox(self.continueInsertFrame,from_=0,to=168,font=('Times',15),validate='all',validatecommand=(self.entryWindow.register(self.spinboxCheck), '%P'))
        self.availableSpinbox.place(relx=0.75,rely=0.7,width=100,height=30)

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
        self.introFunctionFrame()

    # After passing seccessfully the first three fields we end up with the last ones
    require2 = 0 # This also for flag using
    def checkSecondPage(self,user_id):

        if not self.require2:
            self.starSecond = Label(self.continueInsertFrame, text="*(Required)", bg="#99ccff", fg='red', font=("Times", 25))
            # Set the require to 1 so no more label instances are created
            self.require2 += 1

        # Getting the data from the entry instance
        self.checkSecondField = self.activityName.get()

        if not self.checkSecondField:
            self.starSecond.place(relx=0.61, rely=0.26)
        else:
            self.checkSecondField = self.category.get()
            if self.checkSecondField == '-':
                self.starSecond.place(relx=0.11,rely=0.76)
            else:
                self.require2=0
                self.temporaryData = []
                # Adding the last fields to the class list
                self.temporaryData.append(self.activityName.get())
                self.temporaryData.append(self.category.get())
                self.temporaryData.append(int(self.significantScale.get()))
                self.temporaryData.append(int(self.durationSpinbox.get()))
                self.temporaryData.append(int(self.availableSpinbox.get()))


                # Final step is adding to the database depending of the activity category
                if self.temporaryData[1] == "Υποχρεώσεων":
                    self.addCommitmentActivity(user_id,*(self.temporaryData))
                else:
                    self.addLeisureActivity(user_id,*(self.temporaryData))

                self.starSecond.destroy()
                self.addFinished()

    def addFinished(self):

        # After successfully adding the data, we reset everything
        self.temporaryData = []
        self.category.set(value='-')
        self.activityName.delete(0,'end')
        self.significantScale.set(0)
        self.durationSpinbox.delete(0,'end')
        self.durationSpinbox.insert(0,0)
        self.availableSpinbox.delete(0,'end')
        self.availableSpinbox.insert(0,0)


    # A function that checks the range of the spinboxes
    def spinboxCheck(self,text):
        if text:
            try:
                value = int(text)
                if value < 0 or value > 168:
                    return False
            except ValueError:
                return False
        return True



app = introMenu()
