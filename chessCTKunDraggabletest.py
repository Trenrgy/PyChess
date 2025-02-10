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

    def changeTheme(self, theme):
        global felder, felder_links, felder_links
        for feld in felder:
            if (feld.r + feld.z) % 2 == 0:
                i.config(bg=themes[theme][0])
            else:
                i.config(bg=themes[theme][1])


"""
Klassen für den Singleplayer-Spielmodus

SplitScreen-Klasse:
Diese Klasse ist der Hauptknoten des Singleplayer-Spielmodus
"""


class SplitScreen(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.seite = 0
        self.place(relx=0.1, rely=0, relwidth=0.9, relheight=1, anchor="nw")

        # Schachbretter
        global felder_links, felder_rechts
        self.links = Board(master=self, felder=felder_links)  # Verwende felder_links
        self.links.place(relx=0.05, rely=0.4, anchor="w")

        self.rechts = Board(master=self, felder=felder_rechts)  # Verwende felder_rechts
        self.rechts.place(relx=0.9, rely=0.4, anchor="e")

        self.changeSideButton = ctk.CTkButton(self, text="\u21C6", command=self.reset, font=("", 30), width=3, height=3)
        self.changeSideButton.place(relx=0.474, rely=0.8, anchor="center")
        self.reset()

    def reset(self):
        if self.seite == 0:
            self.links.reset("black")
            self.rechts.reset("white")
            self.seite = 1
        else:
            self.links.reset("white")
            self.rechts.reset("black")
            self.seite = 0


def openSingleplayer():
    split.tkraise()


"""Klasse für das Spielfeld"""
felder = [[], [], [], [], [], [], [], []]


# zwei separate globale Listen für beide Bretter
felder_links = [[], [], [], [], [], [], [], []]
felder_rechts = [[], [], [], [], [], [], [], []]


class Board(ctk.CTkFrame):
    def __init__(self, master, felder):
        super().__init__(master)
        self.bgColor = "green"

        self.felder = felder

        # Felder erstellen
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 != 0:
                    self.felder[i].append(Felder(self, i, j, _themes["dark-green"][0]))
                else:
                    self.felder[i].append(Felder(self, i, j, _themes["dark-green"][1]))

    def reset(self, side):
        n = 0 if side == "black" else 6

        # Bilder entfernen
        for r in range(8):
            for z in range(8):
                self.felder[r][z].resetImg()

        # Figuren setzen
        for z in range(8):  # Bauern
            self.felder[1][z].figurSetzen(10 - n)
            self.felder[6][z].figurSetzen(4 + n)

        self.felder[7][3].figurSetzen(0 + n)  # Damen
        self.felder[0][3].figurSetzen(6 - n)
        self.felder[7][4].figurSetzen(1 + n)  # Könige
        self.felder[0][4].figurSetzen(7 - n)

        self.felder[7][0].figurSetzen(5 + n)
        self.felder[7][7].figurSetzen(5 + n)
        self.felder[0][0].figurSetzen(11 - n)
        self.felder[0][7].figurSetzen(11 - n)

        self.felder[7][1].figurSetzen(2 + n)
        self.felder[7][6].figurSetzen(2 + n)
        self.felder[0][1].figurSetzen(8 - n)
        self.felder[0][6].figurSetzen(8 - n)

        self.felder[7][2].figurSetzen(3 + n)
        self.felder[7][5].figurSetzen(3 + n)
        self.felder[0][2].figurSetzen(9 - n)
        self.felder[0][5].figurSetzen(9 - n)

    def changeTheme(self, theme):
        self.bgColor = theme
        for i in self.felder:
            for j in i:
                j.config(bg=self.bgColor)


"""Klasse für die Felder auf dem Spielfeld"""
istAmZug = 0

class Felder(ctk.CTkCanvas):
    def __init__(self, master, r, z, bgcolor):
        super().__init__(master, height=65, width=65, bg=bgcolor, highlightthickness=0)
        self.bind("<Button-1>", self.zuegePruefen)
        self.r = r
        self.z = z
        self.grid(row=r, column=z)
        self.figurNr = None

        # Referenz auf globale Figuren
        global figuren
        self.bild_id = None

    def figurSetzen(self, figurNr):
        """Figuren im Canvas anzeigen"""
        self.figurNr = figurNr
        if self.bild_id is not None:
            self.delete(self.bild_id)
        self.bild_id = self.create_image(
            32.5, 32.5, image=figuren[figurNr], anchor="center"
        )

    def resetImg(self):
        """Bild entfernen"""
        if self.bild_id is not None:
            self.delete(self.bild_id)

    def orthogonale(self, r, z):
        """Orthogonale prüfen"""
        moeglicheZuege = []
        schlagbar = []

        global felder
        exit = False
        while not exit:
            r += 1
            if felder[r][z].figurNr is None and r <= 7:
                moeglicheZuege.append((r, z))
            elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                moeglicheZuege.append((r, z))
                schlagbar.append((r, z))
            else:
                exit = True
        r = self.r
        while not exit:
            r -= 1
            if felder[r][z].figurNr is None and 0 <= r:
                moeglicheZuege.append((r, z))
            elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                moeglicheZuege.append((r, z))
                schlagbar.append((r, z))
            else:
                exit = True
        while not exit:
            z += 1
            if felder[r][z].figurNr is None and z <= 7:
                moeglicheZuege.append((r, z))
            elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                moeglicheZuege.append((r, z))
            else:
                exit = True
        z = self.z
        while not exit:
            z -= 1
            if felder[r][z].figurNr is None and 0 <= z:
                moeglicheZuege.append((r, z))
            elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                moeglicheZuege.append((r, z))
                schlagbar.append((r, z))
            else:
                exit = True

        return moeglicheZuege, schlagbar

    def diagonale(self, r, z):
        """Diagonale prüfen"""
        moeglicheZuege = []
        schlagbar = []

        exit = False
        while not exit:

            if (r + 1) <= 7 and (z + 1) <= 7:
                r += 1
                z += 1
                if felder[r][z].figurNr is None:
                    moeglicheZuege.append((r, z))
                elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                    moeglicheZuege.append((r, z))
                    schlagbar.append((r, z))
                else:
                    exit = True
            else:
                exit = True
        r = self.r
        z = self.z
        exit = False
        while not exit:

            if (r - 1) >= 0 and (z + 1) <= 7:
                r -= 1
                z += 1
                print(r, z)
                if felder[r][z].figurNr is None:
                    moeglicheZuege.append((r, z))
                elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                    moeglicheZuege.append((r, z))
                    schlagbar.append((r, z))
                else:
                    exit = True
            else:
                exit = True
        r = self.r
        z = self.z
        exit = False
        while not exit:

            if (r + 1) >= 0 and (z - 1) <= 7:
                r += 1
                z -= 1
                if felder[r][z].figurNr is None:
                    moeglicheZuege.append((r, z))
                elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                    moeglicheZuege.append((r, z))
                    schlagbar.append((r, z))
                else:
                    exit = True
            else:
                exit = True
        r = self.r
        z = self.z
        exit = False
        while not exit:

            if (r - 1) >= 0 and (z - 1) >= 0:
                r -= 1
                z -= 1
                if felder[r][z].figurNr is None and 0 <= r and 0 <= z:
                    moeglicheZuege.append((r, z))
                elif felder[r][z].figurNr > 5 >= self.figurNr or felder[r][z].figurNr <= 5 < self.figurNr:
                    moeglicheZuege.append((r, z))
                    schlagbar.append((r, z))
                else:
                    exit = True
            else:
                exit = True

        return moeglicheZuege, schlagbar

    def moeglicheZuege(self):
        r = self.r
        z = self.z
        moeglicheZuege = []
        schlagbar = []

        # Zugriff auf korrekte globale Felderliste basierend auf dem Elternlayout
        global felder_links, felder_rechts
        felder = felder_links if isinstance(self.master,
                                            Board) and self.master.felder == felder_links else felder_rechts

        # Logik für mögliche Züge
        if self.figurNr == 0 or self.figurNr == 6:  # Dame Züge suchen
            moeglicheZuege, schlagbar = self.diagonale(r, z)
            moeglicheZuege2, schlagbar2 = self.orthogonale(r, z)
            moeglicheZuege += moeglicheZuege2
            schlagbar += schlagbar2

        elif self.figurNr == 1 or self.figurNr == 7:  #König Züge prüfen
            if r-1 >= 0:
                if felder[r][z].figurNr is None:
                    moeglicheZuege.append((r, z))
            if r+1 <= 7:
                if felder[r][z].figurNr is None:
                    moeglicheZuege.append((r, z))
            if z-1 >= 0:
                if felder[r][z].figurNr is None:
                    moeglicheZuege.append((r, z))
            if z+1 <= 7:
                if felder[r][z].figurNr is None:
                    moeglicheZuege.append((r, z))

        elif self.figurNr == 2 or self.figurNr == 8:  # Läufer Züge prüfen
            moeglicheZuege, schlagbar = self.diagonale(r, z)

        elif self.figurNr == 3 or self.figurNr == 9:  # Springer Züge prüfen
            if not ((r + 2) > 7):
                if felder[r + 2][z].figurNr is None:
                    moeglicheZuege.append((r + 2, z))
                    if self.figurNr > 5 >= felder[r + 2][z + 1].figurNr or self.figurNr <= 5 < felder[r + 2][z + 1].figurNr:
                        schlagbar.append((r + 2, z + 1))
                    if self.figurNr > 5 >= felder[r + 2][z - 1].figurNr or self.figurNr <= 5 < felder[r + 2][z - 1].figurNr:
                        schlagbar.append((r + 2, z - 1))
            if not ((r - 2) < 0):
                if felder[r - 2][z].figurNr is None:
                    moeglicheZuege.append((r - 2, z))
                    if self.figurNr > 5 >= felder[r - 2][z + 1].figurNr or self.figurNr <= 5 < felder[r - 2][z + 1].figurNr:
                        schlagbar.append((r - 2, z + 1))
                    if self.figurNr > 5 >= felder[r - 2][z - 1].figurNr or self.figurNr <= 5 < felder[r - 2][z - 1].figurNr:
                        schlagbar.append((r - 2, z - 1))
            if not ((z + 2) > 7):
                if felder[r + 1][z + 2].figurNr is None:
                    moeglicheZuege.append((r + 1, z + 2))
                    if self.figurNr > 5 >= felder[r + 1][z + 3].figurNr or self.figurNr <= 5 < felder[r + 1][z + 3].figurNr:
                        schlagbar.append((r + 1, z + 3))
                    if self.figurNr > 5 >= felder[r + 1][z - 1].figurNr or self.figurNr <= 5 < felder[r + 1][z - 1].figurNr:
                        schlagbar.append((r + 1, z - 1))
            if not ((z - 2) < 0):
                if felder[r + 1][z - 2].figurNr is None:
                    moeglicheZuege.append((r + 1, z - 2))
                    if self.figurNr > 5 >= felder[r + 1][z + 1].figurNr or self.figurNr <= 5 < felder[r + 1][z + 1].figurNr:
                        schlagbar.append((r + 1, z + 1))
                    if self.figurNr > 5 >= felder[r + 1][z - 3].figurNr or self.figurNr <= 5 < felder[r + 1][z - 3].figurNr:
                        schlagbar.append((r + 1, z - 3))


        elif self.figurNr == 4 or self.figurNr == 10:
            if r == 1:
                if felder[r + 2][z].figurNr is None:
                    moeglicheZuege.append((r + 2, z))
            elif r == 6:
                if felder[r - 2][z].figurNr is None:
                    moeglicheZuege.append((r - 2, z))

            if self.figurNr > 5 >= felder[r + 1][z + 1].figurNr or self.figurNr <= 5 < felder[r + 1][z + 1].figurNr:
                schlagbar.append((r + 1, z + 1))
            if self.figurNr > 5 >= felder[r + 1][z - 1].figurNr or self.figurNr <= 5 < felder[r + 1][z - 1].figurNr:
                schlagbar.append((r + 1, z - 1))
            if felder[r + 1][z].figurNr is None:
                moeglicheZuege.append((r + 1, z))

        print(moeglicheZuege)
        return moeglicheZuege


    def zuegePruefen(self, event):
        """Aktion beim Klicken - Testfunktion"""
        if self.bild_id is not None:
            if self.figurNr is not None:
                self.moeglicheZuege()
                self.create_oval(10, 10, 60, 60)


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

