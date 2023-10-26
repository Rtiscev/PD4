import os


def fixString(source):
    prepareStr = source.split("/")
    if len(prepareStr[1]) < 2:
        source = prepareStr[0] + "/" + "0" + prepareStr[1]
    return source


def firstFunc(datetime_object, path):
    # first model
    # from dataset.csv
    isFound = False
    isChanged = False
    f = open(path, "r")
    lines = f.readlines()
    arr = []
    string = ""

    for i in range(len(lines)):
        sliced = lines[i].split(",")

        # get current month and year
        year = sliced[0].split("/")[0]
        month = sliced[0].split("/")[1]

        if isFound == False and isChanged == True:
            break

        if datetime_object.year == int(year) and datetime_object.month == int(month):
            # prepare array with the Data from file
            for rr in range(len(sliced)):
                if rr > 0 and rr < len(sliced) - 1:
                    string += sliced[rr] + ","
                elif rr > 0:
                    string += sliced[rr]
            # append the string
            arr.append(string)

            if isFound == False:
                isFound = True
            isChanged = True

        string = ""

    return arr


def firstAnn(path, datasetPath):
    f = open(datasetPath, "r")
    lines = f.readlines()

    if not os.path.exists(f"{path}/files"):
        os.makedirs(f"{path}/files")

    # if it exists, delete it
    if os.path.exists(f"{path}/files/X.csv"):
        os.remove(f"{path}/files/X.csv")
    if os.path.exists(f"{path}/files/Y.csv"):
        os.remove(f"{path}/files/Y.csv")

    X = open(f"{path}/files/X.csv", "a")
    Y = open(f"{path}/files/Y.csv", "a")

    for line in lines:
        txt = line.split(",")
        i = 0
        string = ""
        for text in txt:
            if i == 0:
                X.write(f"{text}/n")
            elif i == len(txt) - 1:
                string += text
            else:
                string += text + ","
            i += 1
        Y.write(string)

    X.close()
    Y.close()


def secondAnn(path, datasetPath):
    f = open(datasetPath, "r")
    lines = f.readlines()

    arr = []
    hashset = set()
    actualYear = ""
    lastMonth = ""
    fMonth = ""
    string = ""

    if not os.path.exists(f"{path}/files/months"):
        os.makedirs(f"{path}/files/months")

    for i in range(len(lines)):
        # get the I'th line from the file and split it
        sliced = lines[i].split(",")

        # get current Year
        actualYear = sliced[0]
        # save only the year
        hashset.add(actualYear.split("/")[0])

        # save first Month
        if arr == []:
            fMonth = actualYear

        # prepare array with the Data from file
        for rr in range(len(sliced)):
            if rr > 0 and rr < len(sliced) - 1:
                string += sliced[rr] + ","
            elif rr > 0:
                string += sliced[rr]
            elif rr == 0:
                temp = actualYear.split("/")
                if len(temp[1]) < 2:
                    string += "0" + temp[1] + ","
                else:
                    string += temp[1] + ","
        # append the string
        arr.append(string)

        # get next Year
        if i < len(lines) - 1:
            nextYear = lines[i + 1].split(",")[0]
        else:
            nextYear = "EOF"

        if nextYear.split("/")[0] not in hashset or nextYear == "EOF":
            actualYear = fixString(actualYear)
            endOfYear = fixString(fMonth)

            fName = actualYear.replace("/", "") + "_" + endOfYear.replace("/", "")
            with open(f"{path}/files/months/{fName}.csv", "w") as file:
                for item in arr:
                    file.write(item)

            arr = []

        string = ""


def thirdAnn(path, datasetPath):
    f = open(datasetPath, "r")
    lines = f.readlines()

    arr = []
    hashset = set()
    hashset2 = set()
    actualYear = ""
    lastMonth = ""
    fMonth = ""
    string = ""
    weekCounter = 0
    fDay = 0

    if not os.path.exists(f"{path}/files/weeks"):
        os.makedirs(f"{path}/files/weeks")

    for i in range(len(lines)):
        # get the I'th line from the file and split it
        sliced = lines[i].split(",")

        # get current Year
        actualYear = sliced[0]

        if actualYear.split("/")[0] not in hashset:
            hashset2.clear()
        # save only the month
        hashset2.add(actualYear.split("/")[1])

        # save only the year
        hashset.add(actualYear.split("/")[0])

        # save first Month
        if arr == []:
            fDay = sliced[1]
            fMonth = actualYear

        # prepare array with the Data from file
        for rr in range(len(sliced)):
            if rr > 0 and rr < len(sliced) - 1:
                string += sliced[rr] + ","
            elif rr > 0:
                string += sliced[rr]
        # append the string
        arr.append(string)

        # go next week
        weekCounter += 1

        # get next Year
        if i < len(lines) - 1:
            nextYear = lines[i + 1].split(",")[0]
        else:
            nextYear = "EOF"

        # if reached the end of file or the nextYear has not been added to the set
        if (
            nextYear.split("/")[0] not in hashset
            or nextYear.split("/")[1] not in hashset2
            or nextYear == "EOF"
            or weekCounter == 7
        ):
            actualYear = (
                fixString(actualYear) + "/" + (fDay if len(fDay) == 2 else "0" + fDay)
            )
            endOfYear = (
                fixString(fMonth)
                + "/"
                + (sliced[1] if len(sliced[1]) == 2 else "0" + sliced[1])
            )

            # concatenate the string with new and old date
            fName = actualYear.replace("/", "") + "_" + endOfYear.replace("/", "")

            # open file and write to it
            with open(f"{path}/files/weeks/{fName}.csv", "w") as file:
                for item in arr:
                    file.write(item)

            # nullify the array
            arr = []

            # nullify the weekCounter
            weekCounter = 0

        # nullify the string after the loop iteration (always)
        string = ""
