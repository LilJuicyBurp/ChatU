# Steven Deng
# sdeng5@uci.edu
# 47704456
import tkinter as tk
import a5_gui


def main():
    messenger = tk.Tk()
    messenger.title("ICS 32 Distributed Social Messenger")
    messenger.geometry("720x480")
    messenger.option_add('*tearOff', False)
    messenger.update()
    messenger.minsize(messenger.winfo_width(), messenger.winfo_height())
    app = a5_gui.MainApp(messenger)
    messenger.after(5000, app.check_new)
    messenger.mainloop()

if __name__ == '__main__':
    main()