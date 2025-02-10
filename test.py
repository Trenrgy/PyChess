import customtkinter as ctk


class Root(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="yellow")
        self.title("Chess")
        self.geometry("1920x1080+0+0")


class Multiplayer(ctk.CTkCanvas):
    def __init__(self, master):
        super().__init__(master=master, fg_color=master._fg_color)

        # Das Canvas platzieren
        self.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8, anchor="nw")

    def erstelleFelder(self):
        pass


if __name__ == '__main__':
    root = Root()
    multiplayer = Multiplayer(root)
    root.mainloop()
