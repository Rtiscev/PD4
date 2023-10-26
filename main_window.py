import os
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from functions import *
import datetime

# global variables
isFileSelected = False
currentDate = datetime.datetime.today()
thePath = "None"


def getDate():
    st.delete(index1=1.0, index2="end")

    rawData = cal.get_date().split("/")
    actualData = datetime.datetime(2000 + int(rawData[2]), int(rawData[0]), 1)

    index = 0
    if thePath != "None":
        response = firstFunc(actualData, thePath)
        if response is not []:
            for item in response:
                print(item)
                st.insert("end", item)
        else:
            st.insert("end", "None")


def create_notations():
    firstAnn(folderPath, thePath)
    secondAnn(folderPath, thePath)
    thirdAnn(folderPath, thePath)


def open_folder():
    global folderPath
    folderPath = fd.askdirectory(initialdir=os.getcwd())
    buttonPrepareAnnotations.config(state="active")


def open_file():
    global thePath
    filetypes = (("text files", "*.csv"), ("All files", "*.*"))

    filename = fd.askopenfilename(
        title="Open a file", initialdir=os.getcwd(), filetypes=filetypes
    )

    if filename.find("dataset.csv") != -1:
        showinfo(title="Selected File", message=filename)
        thePath = filename
        buttonDate.config(state="active")
        buttonPath.config(state="disabled")
        buttonPathAnnotations.config(state="active")
    else:
        showinfo(title="Error", message="wrong file")


# root window
root = Tk()
root.geometry("800x400")
root.title("4th Assignment")


left_frame = Frame(root)
right_frame = Frame(root)

left_frame.grid(row=0, column=0)
right_frame.grid(row=0, column=1)

# left frame
labelPath = Label(left_frame, text="Choose date")
buttonPath = Button(left_frame, text="Open file", command=open_file)
labelDate = Label(left_frame, text="Choose path to the dataset")
cal = Calendar(
    left_frame,
    selectmode="day",
    year=currentDate.year,
    month=currentDate.month,
    day=currentDate.day,
)
buttonDate = Button(left_frame, text="Get data", command=getDate, state="disabled")
labelAnnotations = Label(left_frame, text="Annotations to files")
buttonPathAnnotations = Button(
    left_frame,
    text="Set folder path for annotations",
    state="disabled",
    command=open_folder,
)
buttonPrepareAnnotations = Button(
    left_frame, text="Create annotations", state="disabled", command=create_notations
)

# right frame
st = ScrolledText(right_frame, width=60)


# left frame
labelPath.pack()
buttonPath.pack()
labelDate.pack()
cal.pack()
buttonDate.pack()
labelAnnotations.pack()
buttonPathAnnotations.pack()
buttonPrepareAnnotations.pack()
# right frame
st.pack()


# firstFunc()

root.mainloop()

# print(isFileSelected)
