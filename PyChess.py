import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk


"""
Themes für das Schachbrett:
Die Themes für das Schachbrett sind in dictionaries gespeichert, 
damit man mit einem Begriff gleich mehrere Farben speichern kann.
"""


_themes: dict[str, tuple[str, str]] = {
    "purple": ("#ffffff", "#2f0a5c"),
    "dark-blue": ("#ffffff", "#1b1270"),
    "light-blue": ("#ffffff", "#3aaccf"),
    "dark-green": ("#ffffff", "#0f8a32"),
    "gray": ("#ffffff", "#616161"),
    "dark-red": ("#ffffff", "#47020d")}


"""
Root Klasse:
Die Root Klasse ist für das Hauptmenü verantwortlich
"""


class Root(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chess")
        self.geometry("1920x1080+0+0")

        self.seitenmenu = SeitenMenu(self)


"""
Seiten-menu Klasse:
In dieser Klasse wird das Seitenleisten-menu verwaltet
"""


class SeitenMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.place(relx=0, rely=0, relwidth=0.05, relheight=1, anchor="nw")
        self.expanded = False

        # Navigation
        self.optionButton = ctk.CTkButton(self, text="\u2699", font=("", 40), command=self.openOptions)
        self.optionButton.place(relx=0.1, rely=0.9, anchor="nw", relwidth=0.8, relheight=0.07)
        self.singleplayerButton = ctk.CTkButton(self, text="S", font=("", 40), command=openSingleplayer)
        self.singleplayerButton.place(relx=0.1, rely=0.1, anchor="nw", relwidth=0.8, relheight=0.07)

        # expand-Buttons
        self.changeSizeButton = ctk.CTkButton(self, text=">", font=("", 30), width=7, command=self.expandMenu)
        self.changeSizeButton.place(relx=1.0, rely=0.5, anchor="e", relheight=0.05)

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

    def openSingleplayer(self):
        split.tkraise()
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
        self.button1 = ctk.CTkButton(self, text="lila")
        self.button1.place(relx=0.5, rely=0.3, anchor="center")
        self.button2 = ctk.CTkButton(self, text="-dunkelblau")
        self.button2.place(relx=0.5, rely=0.4, anchor="center")
        self.button3 = ctk.CTkButton(self, text="hellblau")
        self.button3.place(relx=0.5, rely=0.5, anchor="center")
        self.button4 = ctk.CTkButton(self, text="dunkelgrün")
        self.button4.place(relx=0.5, rely=0.6, anchor="center")
        self.button5 = ctk.CTkButton(self, text="grau")
        self.button5.place(relx=0.5, rely=0.7, anchor="center")
        self.button6 = ctk.CTkButton(self, text="dunkelrot")
        self.button6.place(relx=0.5, rely=0.8, anchor="center")


"""
Klassen für den Singleplayer-Spielmodus

SplitScreen-Klasse:
Diese Klasse ist der Hauptknoten des Singleplayer-Spielmodus
"""


class SplitScreen(ctk.CTkCanvas):
    def __init__(self, master=None):
        super().__init__(master)
        self.place(relx=0.1, rely=0, relwidth=0.9, relheight=1, anchor="nw")
        self.button = ctk.CTkButton(self, text="Start", command=self.createBoards)
        self.button.place(relx=0.5, rely=0.5, anchor="center")
        self.feld = ctk.CTkLabel(self, fg_color="yellow")
        self.feld.place(relx=0.1, rely=0.1, anchor="nw")

    def createBoards(self):
        felder = []
        hoehe = self.winfo_height()
        breite = self.winfo_width()
        feldHoehe  = hoehe * 0.6
        if breite >= feldHoehe:
            self.feld.configure(height=feldHoehe * 0.6, width=feldHoehe)
        else:
            self.feld.configure(height=breite * 0.6, width=breite * 0.6)

        print(breite, hoehe)


def openSingleplayer():
    split.tkraise()


"""Klasse für das Spielfeld"""
felder = [[], [], [], [], [], [], [], []]


if __name__ == "__main__":
    # CustomTkinter Theme und Modus setzen
    ctk.set_appearance_mode("dark")  # Light oder Dark
    ctk.set_default_color_theme("blue")  # Farbe des Themes

    # Root Fenster initiation
    root = Root()

    # Options Fenster initiation
    options = Options()

    figuren = [
        ImageTk.PhotoImage(Image.open("DameSchwarz.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("KönigSchwarz.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("LäuferSchwarz.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("SpringerSchwarz.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("BauerSchwarz.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("TurmSchwarz.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("DameWeiss.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("KönigWeiss.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("LäuferWeiss.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("SpringerWeiss.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("BauerWeiss.png").resize((60, 60))),
        ImageTk.PhotoImage(Image.open("TurmWeiss.png").resize((60, 60))),
    ]

    # Singleplayer initiation
    split = SplitScreen(root)
    root.seitenmenu.tkraise()
    root.mainloop()

