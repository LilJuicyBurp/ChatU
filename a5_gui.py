# Steven Deng
# sdeng5@uci.edu
# 47704456
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
import pathlib
import time
import ds_messenger
import Profile

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        index = self.posts_tree.focus()
        entry = self.posts_tree.item(index)['text']
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        else:
            entry = contact
        id = self.posts_tree.insert('', id, id, text=entry)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)
    
    def reset_ui(self):
        self.message_editor.delete(1.0, tk.END)
        self.entry_editor.delete(1.0, tk.END)
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250, bg='light blue')
        posts_frame.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.heading('#0', text='Friend List')
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg='light blue')
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg='light blue')
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, width=10, bg='light blue')
        scroll_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        message_frame = tk.Frame(master=self, bg='light blue')
        message_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.message_editor = tk.Text(message_frame, width=0, height=5, bg='light gray')
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=5, pady=5)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right', font='"Comic Sans MS" 10 bold')
        self.entry_editor.tag_configure('entry-left', justify='left', font='"Comic Sans MS" 10 bold')
        self.entry_editor.tag_configure('entry-right-time', justify='right', font='"Comic Sans MS" 8 normal')
        self.entry_editor.tag_configure('entry-left-time', justify='left', font='"Comic Sans MS" 8 normal')
        self.entry_editor.tag_configure('entry-mid', justify='center', font='"Comic Sans MS" 11 bold')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.RIGHT,
                               expand=True, padx=5, pady=5)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.RIGHT,
                                    expand=False, padx=0, pady=5)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.insert(tk.END, self.user)
        self.password_entry.pack()


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.profile = None
        self.direct_messenger = ds_messenger.DirectMessenger()
        self._draw()

    def send_message(self):
        # You must implement this!
        msg = self.body.message_editor.get('1.0', 'end').rstrip()
        self.body.message_editor.delete(1.0, tk.END)
        recp = self.recipient
        direct_message = {'message': msg, 'recipient': recp,
                          'timestamp': time.time()}
        self.profile.sent.append(direct_message)
        boo = self.direct_messenger.send(msg, recp)
        self.profile.save_profile(self._path)
        self.recipient_selected(self.recipient)


    def add_contact(self):
        name = tk.simpledialog.askstring(title = 'New Contact',
                                         prompt = 'Username of New Contact:')
        self.profile.friends.append(name)
        self.profile.save_profile(self._path)
        self.body.insert_contact(name)

    def recipient_selected(self, recipient):
        self.body.entry_editor.config(state='normal')
        self.body.entry_editor.delete(1.0, tk.END)
        self.recipient = recipient
        msg_list = []
        for i in self.profile.get_messages():
            if i.recipient == self.recipient:
                msg = {'type': 'message', 'content': i}
                msg_list.append(msg)
        for i in self.profile.get_sent():
            if i.recipient == self.recipient:
                msg = {'type': 'sent', 'content': i}
                msg_list.append(msg)
        if len(msg_list) == 0:
            return
        msg_list.sort(key = lambda x: float(x['content'].timestamp), reverse=True)
        msg_time = time.strftime('%Y-%m-%d %I %p', time.localtime(float(msg_list[0]['content'].timestamp)))
        for i in msg_list:
            temp_time = time.strftime('%Y-%m-%d %I %p', time.localtime(float(i['content'].timestamp)))
            stamp_time = time.strftime('%Y/%m/%d %I:%M %p', time.localtime(float(i['content'].timestamp)))
            if temp_time != msg_time:
                self.body.entry_editor.insert(1.0, msg_time + '\n', 'entry-mid')
                msg_time = temp_time
            if i['type'] == 'sent':
                self.body.entry_editor.insert(1.0, f'({stamp_time})' + '\n', 'entry-right-time')
                self.body.insert_user_message(i['content'].message)
            else:
                self.body.entry_editor.insert(1.0, f'({stamp_time})' + '\n', 'entry-left-time')
                self.body.insert_contact_message(i['content'].message)
        self.body.entry_editor.insert(1.0, msg_time + '\n', 'entry-mid')
        self.body.entry_editor.config(state='disabled')
        self.body.entry_editor.see('end')


    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger.dsuserver = ud.server
        self.direct_messenger.password = ud.pwd
        self.direct_messenger.username = ud.user

    def publish(self, message:str):
        # You must implement this!
        pass

    def check_new(self):
        if self.direct_messenger.dsuserver is None:
            return
        new_msg = self.direct_messenger.retrieve_new()
        if len(new_msg) > 0:
            for i in new_msg:
                direct_message = {'message': i.message, 'recipient': i.recipient,
                            'timestamp': i.timestamp}
                self.profile.messages.append(direct_message)
            self.profile.save_profile(self._path)
            self.recipient_selected(self.recipient)
        main.after(5000, self.check_new)

    def new_file(self):
        self.body.reset_ui()
        filename = tk.filedialog.asksaveasfilename(filetypes=[('dsu', '*.dsu')])
        ud = NewContactDialog(self.root, "Initiate Account",
                              '', '', '')
        path = pathlib.Path(filename + '.dsu')
        self._path = str(path)
        path.touch()
        self.profile = Profile.Profile(ud.server, ud.user, ud.pwd)
        self.profile.save_profile(path)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger.dsuserver = ud.server
        self.direct_messenger.password = ud.pwd
        self.direct_messenger.username = ud.user
    
    def open_file(self):
        self.body.reset_ui()
        filename = tk.filedialog.askopenfilename(filetypes=[('dsu', '*.dsu')])
        if filename == '':
            return
        self._path = filename
        self.profile = Profile.Profile()
        self.profile.load_profile(filename)
        self.username = self.profile.username
        self.password = self.profile.password
        self.server = self.profile.dsuserver
        self.direct_messenger.dsuserver = self.profile.dsuserver
        self.direct_messenger.password = self.profile.password
        self.direct_messenger.username = self.profile.username
        for i in self.profile.friends:
            self.body.insert_contact(i)
        self.check_new()

    def close(self):
        self.body.reset_ui()
        self.root.destroy()

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_file)
        menu_file.add_command(label='Open...', command=self.open_file)
        menu_file.add_command(label='Close', command=self.close)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.after(5000, app.check_new)
    main.mainloop()
