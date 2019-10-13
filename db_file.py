import wx


class MyFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        box = wx.TextEntryDialog(None, "What do you want to do?")
        answer = "nothing!"
        while box.ShowModal() == wx.ID_OK:
            answer = box.GetValue()
            if "add book " in answer:
                answer = answer[9:]
                self.addBookPub(answer, True)

            elif "find book " in answer:
                answer = answer[10:]
                kind = self.kindRecBook(answer)
                name = self.removeRedd(kind, answer)
                print(self.findBook(name, kind))

            elif "remove book " in answer:
                answer = answer[12:]
                print(answer)
                self.removeBook(answer)

            elif "update book " in answer:
                answer = answer[12:]
                self.updateBook(self.findISBN(answer), self.findUpdate(answer))

            # must be attention to one space and keep the notation that have been held in doc.
            elif "add publisher " in answer:
                answer = answer[14:]
                self.addBookPub(answer, False)

            elif "remove publisher " in answer:
                answer = answer[17:].replace(" ","")
                self.removePublisher(answer)

            elif "update publisher " in answer:
                answer = answer[17:]
                self.updatePubisher(answer)

            elif "find publisher " in answer:
                answer = answer[15:]
                print(self.findPublisher(answer))

        box.Destroy()
        app.Destroy()

    # find publisher by part of its name.
    def findPublisher(self, answer):
        value = answer.split("by")[0].replace(" ", "")
        try:
            with open("Publisher.txt", "r") as fp:
                flag = True
                while flag:
                    line = fp.readline()
                    name = line.split(",")[1].split(":")[1].replace(" ", "")
                    if value in name:
                        flag = False
                        return line.strip()
        except:
            return "Not found in database!"

    # add book by using string as input.
    def addBookPub(self, answer, flag):
        answer = answer.split(", ")
        print(answer)
        book = ","
        book = book.join(answer)
        if flag:
            file = open("books.txt", "a")
        else:
            file = open("Publisher.txt", "a")
        file.write(book + "\n")
        file.close()

    # add book to database by input array to it.
    # if flag is true add to books and else adds to publisher
    def addBookArray(self, array, flag):
        book = ","
        book = book.join(array)
        if flag:
            file = open("books.txt", "a")
        else:
            file = open("Publisher.txt", "a")
        file.write(book + "\n")
        file.close()
        return True
    # main function to find books.
    def findBook(self, name, kind):
        value = kind + ":" + name
        print(value)
        with open("books.txt", "r") as fp:
            flag = True
            while flag:
                line = fp.readline()
                if value in line:
                    flag = False
                    return line.strip()

    # main function to remove book from database.
    def removeBook(self, ISBN):
        book = self.findBook(ISBN, "ISBN")
        print(book)
        s = open("books.txt").read()
        s = s.replace(book, "")
        f = open("books.txt", 'w')
        f.write(s)
        f.close()

    # main function to update data in my database.
    def updateBook(self, ISBN, value):
        counter = 0
        flag = -1
        book = self.findBook(ISBN, "ISBN")
        book = book.split(",")
        kind = value.split(":")[0]
        for bookSpec in book:
            # remove redundant spaces from kind and book by replace function.
            if kind.replace(" ", "") == bookSpec.split(":")[0].replace(" ", ""):
                # flag recognizes index of book specific that should be change.
                flag = counter
            counter += 1
        print("oldBook:", book)
        book[flag] = value.replace(" ", "")
        print("newBook:", book)
        self.removeBook(ISBN)
        self.addBookArray(book, True)

    # find the Kind of book specific using in main find book function.
    def kindRecBook(self, answer):
        if "BookName" in answer:
            return "BookName"
        elif "ISBN" in answer:
            return "ISBN"
        elif "Authors" in answer:
            return "Authors"
        elif "Subjects" in answer:
            return "Subjects"

    # helps to find name of my kind in find book function.
    def removeRedd(self, kind, answer):
        splitter = "by " + kind
        return answer.split(splitter)[0]

    # finds ISBN in update book function.
    def findISBN(self, answer):
        return answer.split("set")[0]

    # split the answer to make search.
    def findUpdate(self, answer):
        answer = answer.split("set")[1]
        (kind, name) = answer.split("to")
        return kind + ":" + name

    # main function to update publisher info.
    def updatePubisher(self, answer):
        pubId = answer.split("set")[0]
        kind = answer.split("set")[1].split("to")[0]
        old = answer.split("set")[1].split("to")[1]
        newValue = (kind + ":" + old).replace(" ", "")
        value = "PubId" + ":" + pubId
        myLine = ""
        counter = 0
        flag1 = True
        with open("Publisher.txt", "r") as fp:
            flag = True
            while flag:
                line = fp.readline()
                if value in line:
                    flag = False
                    myLine = line.strip()
        myLine = myLine.split(",")

        while flag1:
            if kind.replace(" ", "") == myLine[counter].split(":")[0].replace(" ", ""):
                myLine[counter] = newValue
                flag1 = False
                print(myLine[counter])
            counter += 1
        self.removePublisher(pubId)
        if self.addBookArray(myLine,False):
            print("Updated Successfully!")

    def removePublisher(self, pubId):
        value = "PubId:" + pubId
        with open("Publisher.txt", "r+") as fp:
            flag = True
            while flag:
                line = fp.readline()
                if value in line:
                    flag = False
                    myLine = line.strip()

            s = open("Publisher.txt").read()
            s = s.replace(myLine, "")
            f = open("Publisher.txt", 'w')
            f.write(s)
            f.close()



app = wx.App(False)
MyFrame(None)
