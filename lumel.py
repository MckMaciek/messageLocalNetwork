from sys import platform as _platform
from functools import partial
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter.ttk import *
from socket import *
import pandas as pd
import os
import easygui
import csv
 
 
variables = []
textBoxesBelowGroups = []
addressList = {}
listOfChecks = []
listBoxScrollT = []
 
finalSend = []
tosend = []
grupa = [[] for i in range(100000)]
allBut = [[] for i in range(100000)]
 
class RandWtoFile():
    def __init__(self):
        self.txtWithValues = 'data.txt'
        self.txtWithNames = 'data2.txt'
        self.inputIP = ""
        self.inputGroup = ""
        self.stringToFile = ""
 
    def readFromFileToDic(self):
        with open('data.txt') as outfile:
            for line in outfile:
                stringToSplit = line
                stringToSplit = stringToSplit.split(':')
                addressList[stringToSplit[0].replace('\n', '')] = stringToSplit[1].replace('\n', '')
                print(stringToSplit)
 
    def enterNewValue(self):
        while True:
            self.inputIP = str(mainWindow.textBoxIP.get("1.0", END))
            self.inputIP = self.inputIP.replace('\t', '').replace('\n', '')
 
            try:
                self.inputGroup = mainWindow.listBoxGr.get(mainWindow.listBoxGr.curselection())
            except:
                print('-1')
 
            if self.inputGroup != "":
                break
            else:
                continue   # continue untill inputGroup label is not blank
 
        new = {self.inputIP: self.inputGroup}
 
        if self.inputIP not in addressList.keys():
            self.stringToFile = self.inputIP + ":" + self.inputGroup + '\n'
            with open(self.txtWithValues, 'a+') as outfile:
                outfile.write(self.stringToFile)
            addressList.update(new)
 
 
        outfile.close()
        handle(flagToAvoidRessetingTextBoxes)
        mainWindow.textBoxIP.delete('1.0', END)
        mainWindow.window.destroy()
        os.system('python lumel.py')
 
    def removeValue(self):
 
        self.inputIP = str(mainWindow.textBoxIP.get("1.0", END))
        self.inputIP = self.inputIP.replace('\n', '')
        self.inputGroup = mainWindow.listBoxGr.get(mainWindow.listBoxGr.curselection())
 
        outfileDelete = open(self.txtWithValues, "r+")
        allLinesInFile = outfileDelete.readlines()
        outfileDelete.truncate(0)
        outfileDelete.close()
 
        for ipAddress in addressList:
            if ipAddress == self.inputIP:
                for singleListBox in listOfChecks:
                    if ipAddress == singleListBox.cget('text'):
                        singleListBox.destroy()
                        listOfChecks.remove(singleListBox)
            else:
                continue
 
        try:
            del addressList[self.inputIP]
        except:
            print("ERROR -1")
 
        targetStringToDeleteFromFile = self.inputIP + ':' + self.inputGroup + '\n'
 
        if targetStringToDeleteFromFile in allLinesInFile:
            allLinesInFile.remove(targetStringToDeleteFromFile)
 
        with open(self.txtWithValues, "r+") as outfileDelete2:
            for lineInFile in allLinesInFile:
                outfileDelete2.write(lineInFile)
 
        handle(flagToAvoidRessetingTextBoxes)
        mainWindow.textBoxIP.delete('1.0', END)  # AFTER DELETING CHECKBOX, RESET TEXTBOX TO ""
        mainWindow.window.destroy()
        os.system('python lumel.py')
 
    def importExcel(self):
        #df = pd.read_csv('a.csv')
        #lista = list(df)
        Tk().withdraw()
        filename = askopenfilename()
 
        try:
            with open(filename, newline='') as f:
                reader = csv.reader(f)
                data = list(reader)
        except:
            messagebox.showerror("Could not open the file", " Error while opening the file")
            omitFlag = 1
 
 
        if omitFlag == 0:
            iter = 1
            maxIter = len(data)
            numOfEl = len(data)
 
            for j in range(numOfEl):
                maxIter = len(data[j])
                for x in range(maxIter):
                    new = {data[j][iter]: data[j][0]}
                    print(data[j][iter])
                    if self.inputIP not in addressList.keys():
                        self.stringToFile = data[j][iter] + ":" + data[j][0] + '\n'
                        print(self.stringToFile)
                        outfile = open(self.txtWithValues, 'a+')
                        outfile.write(self.stringToFile)
                        outfile.close()
                        addressList.update(new)
                        print(iter)
                    iter += 1
                    if maxIter == iter:
                        break
                iter = 1
 
            handle(flagToAvoidRessetingTextBoxes) # blank
            mainWindow.window.destroy()
            os.system('python lumel.py')
 
        #mainWindow.window.destroy()
        #os.system('python test.py')
 
 
randw = RandWtoFile()
 
class AppWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title = 'Send'
        self.checkOpSys()
        self.screenW, self.screenH = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
 
    def checkOpSys(self):
        if _platform == "linux" or _platform == "linux2":
            self.window.attributes("-zoomed", True)
        elif _platform == "darwin":
            self.window.attributes("-zoomed", True)
        elif _platform == "win32":
            self.window.state('zoomed')
        elif _platform == "win64":
            self.window.state('zoomed')
 
    def createWidgets(self):
 
        self.buttonGroupResize = 45
        self.buttonSendResize = self.buttonGroupResize + 35
        self.buttonAddResize = self.buttonSendResize + 31
 
        self.textBoxIP = Text(self.window, height=1, width=15)
        self.textBoxIP.grid(column=1, row=self.buttonAddResize)
        self.listBoxGr = Listbox(self.window,exportselection=0)
        self.listBoxGr.grid(column=0, row=self.buttonAddResize)
 
        addBtn = Button(self.window, text='Add', command=partial(randw.enterNewValue)).grid(column=0,
                                                                                    row=self.buttonAddResize +3)
        remBtn = Button(self.window, text='Remove', command=partial(randw.removeValue)).grid(column=0,
                                                                                    row=self.buttonAddResize +2)
        impBtn = Button(self.window, text='Import', command=partial(randw.importExcel)).grid(column=0,
                                                                                    row=self.buttonAddResize + 4)
 
mainWindow = AppWindow()
mainWindow.createWidgets()
 
randw.readFromFileToDic()
 
maxAmountOfGroups = 10  ## HOW MANY GROUPS - G1 G2 G3 ETC
flagToAvoidRessetingTextBoxes = False
listBoxScrollTS = []
lbt = [[] for i in range(maxAmountOfGroups)]
impFlag = 0
 
 
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys
 
 
def total_keys(test_dict):
    return (0 if not isinstance(test_dict, dict)
            else len(test_dict) + sum(total_keys(val) for val in test_dict.values()))
 
 
def set_all(value):
    if value == True:
        for idx in listBoxScrollT:
            idx.select_set(0, END)
    else:
        for idx in listBoxScrollT:
            idx.selection_clear(0, END)
 
 
def set_certain(arg):
 
    listBoxScrollTS[arg].select_set(0, END)
 
def checkStatusToSendA(): #defaultowa
    i = 0
    finalSend.clear()
    for x in variables:
        if x.get() == True:
            stringS = tosend[i].cget('text')
            finalSend.append(stringS)
            i += 1
        else:
            i += 1
 
 
numOfKeys = total_keys(addressList)
j = 1
a = 0
 
finalSend = []
tosend = []
grupa = [[] for i in range(100000)]
allBut = [[] for i in range(100000)]
 
tempV = 0
 
 
for x in range(numOfKeys):
    j = 1
    a = 0
 
gr = []
 
for i in range(maxAmountOfGroups):
    gr.append("G" + str(i))
 
for item in gr:
    mainWindow.listBoxGr.insert(END, item)
    mainWindow.listBoxGr.select_set(0)
 
 
#yscrollbar = Scrollbar(mainWindow.window)
#yscrollbar.pack(side = RIGHT, fill = Y)
 
 
def handle(flagToAvoidRessetingTextBoxes):
    j = 1
    a = 0
 
    c = 0
 
    for x in range(maxAmountOfGroups):
 
        listBoxScroll = Listbox(mainWindow.window, selectmode="multiple", exportselection=0)
        listBoxScroll.grid(column=x, row=j)
        listBoxScrollT.append(listBoxScroll)
        listBoxScrollTS.append(listBoxScroll)
        print(listBoxScrollTS)
        #lbt.append(listBoxScroll)
        # k = (list(addressList.keys())[list(addressList.values()).index(getKeysByValue(addressList,'G'))])
        try:
            if (x < maxAmountOfGroups):
                knasz = getKeysByValue(addressList, 'G' + str(x))
            else:
                pass
        except:
            pass
 
        #yscrollbar.config(command=window.yview)
 
            # for i in knasz:
        for i in knasz:
            v = BooleanVar()
            variables.append(v)
            grupa[x].append(v)
            if (x < 15):
                c = (Checkbutton(mainWindow.window, text='' + str(i), variable=v))
                listBoxScrollT[x].insert(END,c.cget('text'))
                #listBoxScrollTS[x].insert(END,c)
                lbt[x].append(c.cget('text'))
                #c.grid(column=a, row=j)
                listOfChecks.append(c)
                allBut[x].append(c)
            else:
                pass
            tosend.append(c)
            j = j + 1
 
        j = 1
        a = a + 1
 
        Button(mainWindow.window, text='G' + str(x), command=partial(set_certain, x)).grid(column=x,
                                                                                           row=j + mainWindow.buttonGroupResize)
        if (x < 15):
 
            if flagToAvoidRessetingTextBoxes == False:
                txt = Text(mainWindow.window, height=1, width=15)
                txt.grid(column=x, row=j + mainWindow.buttonGroupResize + 1, pady=5)
                textBoxesBelowGroups.append(txt)
        else:
            pass
        # Button(window, text='Add', command=partial(send, finalSend, tosend)).grid(column=0, row=buttonAddResize)
values = []
 
def checkStatusToSend(finalSend):
    i = 0
    print("TUAJ")
 
    values.clear()
    for x in range(maxAmountOfGroups):
        alltoSend = [listBoxScrollT[x].get(idx) for idx in listBoxScrollT[x].curselection()]
        if len(alltoSend):
            values.extend(alltoSend)
 
    finalSend = values[:]
    alltoSend.clear()
    return finalSend
 
def save():
    savingGroupNameToFile = ""
 
    outfile2 = open('data2.txt', 'r+')
    outfile2.truncate(0)
    outfile2.close()
 
    with open('data2.txt', 'r+') as outfile2:
        for x in range(maxAmountOfGroups):
            savingGroupNameToFile = textBoxesBelowGroups[x].get("1.0", END)
            print("DO PLIKU" + savingGroupNameToFile)
            outfile2.write(savingGroupNameToFile)
 
 
Button(mainWindow.window, text='Check All', command=partial(set_all, True)).grid(column=maxAmountOfGroups - 1,
                                                                      row=mainWindow.buttonAddResize + 20, pady=10)
Button(mainWindow.window, text='Uncheck All', command=partial(set_all, False)).grid(column=maxAmountOfGroups - 2,
                                                                         row=mainWindow.buttonAddResize + 20, pady=10)
 
 
def send(finalSend, toSend):
    msg = "Enter your text to send"
    title = "Sending text to the destinations"
    fieldNames = ["->"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = easygui.multenterbox(msg, title, fieldNames)
 
    finalSend = checkStatusToSend(finalSend)
    handle(flagToAvoidRessetingTextBoxes)
 
    while 1:
 
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        port = 1337
 
        finalSend = list(dict.fromkeys(finalSend))
 
        for x in finalSend:
            print("JEST" + x)
 
            try:
                addr = (x, port)
                UDPSock = socket(AF_INET, SOCK_DGRAM)
 
                data = fieldValues[0]
                data = data.encode('ascii')
                UDPSock.sendto(data, addr)
                UDPSock.close()
            except:
                messagebox.showerror("Message not send", " {} is invalid or unreachable".format(x))
                continue
 
        finalSend.clear()
        tosend.clear()
        listBoxScrollT.clear()
        variables.clear()
        listBoxScrollTS.clear()
        handle(flagToAvoidRessetingTextBoxes)
 
        # os._exit(0)
        fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
        # print("Reply was:", fieldValues)
 
 
handle(flagToAvoidRessetingTextBoxes)
 
flagToAvoidRessetingTextBoxes = True
 
outfile2 = open('data2.txt', 'r+')
for x in range(maxAmountOfGroups):
    for line in outfile2:
        textBoxesBelowGroups[x].insert("end-1c", line.replace("\n", ""))
        break
outfile2.close()
 
numOfKeys = total_keys(addressList)
Button(mainWindow.window, width=20, text='Send', command=partial(send, finalSend, tosend)).grid(column=0, row=mainWindow.buttonAddResize + 20)
Button(mainWindow.window, text='Save', command=partial(save)).grid(column=maxAmountOfGroups - 3, row=mainWindow.buttonAddResize + 20, pady=10)
mainWindow.window.mainloop()
 
