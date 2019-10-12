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
                self.addBook(answer)

            elif "find book " in answer:
                answer = answer[10:]
                kind = self.kindRec(answer)
                name = self.removeRedd(kind, answer)
                print(self.findBook(name, kind))

            elif "remove book " in answer:
                answer = answer[12:]
                print(answer)
                self.removeBook(answer)

            elif "update book " in answer:
                answer = answer[12:]
                self.updateBook(self.findISBN(answer), self.findUpdate(answer))

        box.Destroy()
        app.Destroy()

    # add book by using string as input.
    def addBook(self, answer):
        answer = answer.split(", ")
        print(answer)
        book = ","
        book = book.join(answer)
        file = open("database.txt", "a")
        file.write(book + "\n")
        file.close()

    # add book to database by input array to it.
    def addBookArray(self, array):
        book = ","
        book = book.join(array)
        file = open("database.txt", "a")
        file.write(book + "\n")
        file.close()

    def findBook(self, name, kind):
        value = kind + ":" + name
        print(value)
        with open("database.txt", "r") as fp:
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
        s = open("database.txt").read()
        s = s.replace(book, "")
        f = open("database.txt", 'w')
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
        self.addBookArray(book)

    # find the Kind of book specific using in main find book function.
    def kindRec(self, answer):
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




app = wx.App(False)
MyFrame(None)
app.MainLoop()
