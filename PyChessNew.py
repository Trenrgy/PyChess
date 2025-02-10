from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk

themes = {
    "purple": "#2f0a5c",
    "dark-blue": "#1b1270",
    "light-blue": "#3aaccf",
    "dark-green": "#0f8a32",
    "gray": "#616161",
    "dark-red": "#47020d"
}

class Root(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PyChess")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.minsize(400, 250)
        self.seitenmenu = SeitenMenu(self)
        self.options = Options(self)

class SeitenMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.place(relx=0, rely=0, relwidth=0.05, relheight=1, anchor="nw")
        self.expanded = False

        # Navigation
        self.optionButton = ctk.CTkButton(self, text="\u2699", font=("", 40), command=self.openOptions)
        self.optionButton.place(relx=0.1, rely=0.9, anchor="nw", relwidth=0.8, relheight=0.07)

        # expand-Buttons
        self.changeSizeButton = ctk.CTkButton(self, text=">", font=("", 30), width=7, command=self.expandMenu)
        self.changeSizeButton.place(relx=1.0, rely=0.5, anchor="e", relheight=0.05)

        self.testbutton = ctk.CTkButton(self, command=lambda: chess.drawSplitChess())
        self.testbutton.place(relx=0.5, rely=0.5, anchor="e", relheight=0.05)

    def expandMenu(self):
        """Menu vergrößern / verkleinern"""
        if self.expanded:
            width = 0.1
            for i in range(100):
                width -= 0.0005
                self.place(relx=0, rely=0, relwidth=0.05, relheight=1)
            self.expanded = False
            self.changeSizeButton.configure(text=">")
            self.optionButton.configure(text="\u2699", font=("", 30))
        else:
            width = 0.05
            for i in range(100):
                width += 0.0005
                self.place(relx=0, rely=0, relwidth=width, relheight=1)
            self.expanded = True
            self.changeSizeButton.configure(text="<")
            self.optionButton.configure(text="\u2699 Einstellungen", font=("", 14))

    def openOptions(self):
        options.tkraise()
        self.tkraise()


"""
Klassen für Einstellungen

Options-Klasse:
Diese Klasse fungiert als master für die gesamte Einstellungsseite
"""


class Options(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.place(relx=0.05, rely=0, relwidth=1, relheight=1)
        self.themeButton = ctk.CTkButton(self, text="Theme wechseln", command=self.openThemes)
        self.themeButton.place(relx=0.5, rely=0.3, anchor="center")
        self.themeWindow = ThemeWindow()

    def openThemes(self):
        self.themeWindow.tkraise()


class ThemeWindow(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=None)
        self.place(relx=0.1, rely=0, relwidth=1, relheight=1)

        # verschiedene Themes zum auswählen
        self.button1 = ctk.CTkButton(self, text="lila", command=lambda: self.changeTheme("purple"))
        self.button1.place(relx=0.5, rely=0.3, anchor="center")
        self.button2 = ctk.CTkButton(self, text="-dunkelblau", command=lambda: self.changeTheme("dark-blue"))
        self.button2.place(relx=0.5, rely=0.4, anchor="center")
        self.button3 = ctk.CTkButton(self, text="hellblau", command=lambda: self.changeTheme("light-blue"))
        self.button3.place(relx=0.5, rely=0.5, anchor="center")
        self.button4 = ctk.CTkButton(self, text="dunkelgrün", command=lambda: self.changeTheme("dark-green"))
        self.button4.place(relx=0.5, rely=0.6, anchor="center")
        self.button5 = ctk.CTkButton(self, text="grau", command=lambda: self.changeTheme("gray"))
        self.button5.place(relx=0.5, rely=0.7, anchor="center")
        self.button6 = ctk.CTkButton(self, text="dunkelrot", command=lambda: self.changeTheme("dark-red"))
        self.button6.place(relx=0.5, rely=0.8, anchor="center")


class Chess(ctk.CTkCanvas):
    def __init__(self, master):
        super().__init__(master=master)
        self.bind("<Configure>", self.drawSplitChess)
        self.place(relx=0.1, rely=0, relwidth=0.9, relheight=1, anchor="nw")
        self.felder = [[], [], [], [], [], [], [], []]
        self.felderRechts = [[], [], [], [], [], [], [], []]
        self.drawSplitChess()

    def drawSplitChess(self, event=None):
        if len(self.felder[0]) > 0:
            for reihe in self.felder:
                for feld in reihe:
                    self.delete(feld)

            for reihe in self.felderRechts:
                for feld in reihe:
                    self.delete(feld)

            self.felder = [[], [], [], [], [], [], [], []]
            self.felderRechts = [[], [], [], [], [], [], [], []]

        height = self.winfo_height()
        width = self.winfo_width()
        verhaeltnisBreite = (width * 0.8) / 17
        verhaeltnisHoehe = (height * 0.8) / 8
        print(height, width, verhaeltnisBreite, verhaeltnisHoehe)

        if verhaeltnisBreite < verhaeltnisHoehe:
            felderGroesse = verhaeltnisBreite
        else:
            felderGroesse = verhaeltnisHoehe

        width = width * 0.1
        height = height * 0.1
        for reihe in range(8):
            for z in range(8):
                self.felder[reihe].append(self.create_rectangle(width, height, width + felderGroesse, height + felderGroesse, fill="blue"))
                width = width + felderGroesse
            width = self.winfo_width() * 0.1
            height = height + felderGroesse

        width = self.winfo_width() * 0.55
        height = self.winfo_height() * 0.1
        for reihe in range(8):
            for z in range(8):
                self.felderRechts[reihe].append(self.create_rectangle(width, height, width + felderGroesse, height + felderGroesse, fill="blue"))
                width = width + felderGroesse
            width = self.winfo_width() * 0.55
            height = height + felderGroesse

        print(self.felder)

    def changeTheme(self, theme):
        for reihe in range(8):
            for zeile in range(8):
                if ((reihe + zeile) % 0) > 1:
                    self.felder[reihe][zeile].configure(fill=theme)

if __name__ == "__main__":
    root = Root()
    options = Options(root)
    chess = Chess(root)
    root.seitenmenu.tkraise()
    root.mainloop()