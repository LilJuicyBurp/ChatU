# Steven Deng
# sdeng5@uci.edu
# 47704456
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
    def __init__(self, root, send_callback=None, con=None, add=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._config_callback = con
        self._add_callback = add
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def config(self):
        if self._config_callback is not None:
            self._config_callback()

    def add_click(self):
        if self._add_callback is not None:
            self._add_callback()

    def _draw(self):
        send_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        conf_button = tk.Button(master=self, text="Edit Profile", width=20, command=self.config)
        conf_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        add_button = tk.Button(master=self, text="Add Contact", width=20, command=self.add_click)
        add_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Offline")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, srv=None):
        self.root = root
        self.username = user
        self.password = pwd
        self.server = srv
        super().__init__(root, title)

    def body(self, frame):
        if self.server is not None:
            self.srv_label = tk.Label(frame, width=30, text="DSU Server:")
            self.srv_label.pack()
            self.srv_entry = tk.Entry(frame, width=30)
            self.srv_entry.insert(tk.END, self.server)
            self.srv_entry.pack()
        self.username_label = tk.Label(frame, width=30, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.username)
        self.username_entry.pack()
        self.pwd_label = tk.Label(frame, width=30, text="Password:")
        self.pwd_label.pack()
        self.pwd_entry = tk.Entry(frame, width=30)
        self.pwd_entry['show'] = '*'
        self.pwd_entry.insert(tk.END, self.password)
        self.pwd_entry.pack()

    def apply(self):
        self.username = self.username_entry.get()
        self.password = self.pwd_entry.get()
        if self.server is not None:
            self.server = self.srv_entry.get()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.current_msgs = []
        self.recipient = None
        self.profile = None
        self.status = False
        self.direct_messenger = ds_messenger.DirectMessenger()
        self._draw()

    def send_message(self):
        msg = self.body.message_editor.get('1.0', 'end').rstrip()
        self.body.message_editor.delete(1.0, tk.END)
        recp = self.recipient
        direct_message = {'message': msg, 'recipient': recp,
                          'timestamp': time.time()}
        self.profile.sent.append(direct_message)
        boo = self.direct_messenger.send(msg, recp)
        if boo == False:
            messagebox.showerror('ERROR!',
                                 'Message Not Sent')
            return
        self.profile.save_profile(self._path)
        self.recipient_selected(self.recipient)

    def add_contact(self):
        name = tk.simpledialog.askstring(title = 'New Contact',
                                         prompt = 'Username of New Contact:')
        if name == None:
            return
        if name == '':
            messagebox.showerror('Missing Info!', 'Friend Not Added')
            return
        num = 0
        for n in name:
            if n != ' ':
                num += 1
        if num == 0:
            messagebox.showerror('Missing Info!', 'Friend Not Added')
            return
        self.profile.friends.append(name)
        self.profile.save_profile(self._path)
        self.body.insert_contact(name)

    def save_entry(self):
        for i in self.current_msgs:
            if i.recipient == self.recipient:
                i.message = self.body.message_editor.get('1.0', 'end').rstrip()
                self.body.message_editor.delete(1.0, tk.END)
                return
        unfinished_msg = ds_messenger.DirectMessage()
        unfinished_msg.message = self.body.message_editor.get('1.0', 'end').rstrip()
        unfinished_msg.recipient = self.recipient
        self.current_msgs.append(unfinished_msg)
        self.body.message_editor.delete(1.0, tk.END)
        return

    def recipient_selected(self, recipient):
        self.body.entry_editor.config(state='normal')
        self.body.entry_editor.delete(1.0, tk.END)
        self.save_entry()
        self.recipient = recipient
        for i in self.current_msgs:
            if i.recipient == self.recipient:
                self.body.set_text_entry(i.message)
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
        ud = NewContactDialog(self.root, "Configure Account", self.username,
                              self.password)
        if ud.username is None or ud.password is None:
                return
        ud.server = self.server
        if not self.info_check(ud):
            messagebox.showerror('Missing Info!', 'Profile Not Changed')
            return
        self.username = ud.username
        self.password = ud.password
        self.direct_messenger.password = ud.password
        self.direct_messenger.username = ud.username
        self.profile.password = ud.password
        self.profile.username = ud.username
        self.profile.save_profile(self._path)

    def check_new(self):
        if self.direct_messenger.dsuserver is None:
            return
        new_msg = self.direct_messenger.retrieve_new()
        if len(new_msg) > 0:
            for i in new_msg:
                direct_message = {'message': i.message, 'recipient': i.recipient,
                            'timestamp': i.timestamp}
                self.profile.messages.append(direct_message)
                if i.recipient not in self.profile.friends:
                    self.profile.friends.append(i.recipient)
                    self.body.insert_contact(i.recipient)
            self.profile.save_profile(self._path)
            self.recipient_selected(self.recipient)
        main.after(5000, self.check_new)

    def info_check(self, user):
        try:
            if user.username == '' or user.password == '' or user.server == '':
                return False
            if user.username is None or user.password is None or user.server is None:
                return False
            info_list = [user.username, user.password, user.server]
            for i in info_list:
                num = 0
                for n in i:
                    if n != ' ':
                        num += 1
                if num == 0:
                    return False
            return True
        except:
            return False

    def new_file(self):
        if self.status == True:
            self.body.reset_ui()
        filename = tk.filedialog.asksaveasfilename(filetypes=[('dsu', '*.dsu')])
        if filename == '':
            messagebox.showerror('No File selected!',
                                 'User Not Created')
            return
        ud = NewContactDialog(self.root, "Initiate Account",
                              '', '', '')
        if not self.info_check(ud):
            messagebox.showerror('Missing Creation Info!',
                                 'User Not Created')
            return
        elif self.status == False:
            self.starter_frame.destroy()
            self.starter_frame1.destroy()
            self.welcome_msg.destroy()
            self.welcome_msg1.destroy()
            self.new_button.destroy()
            self.old_button.destroy()
            self.status = True
            self.main_program()
        self.profile = Profile.Profile(ud.server, ud.username, ud.password)
        self.username = ud.username
        self.password = ud.password
        self.server = ud.server
        self.direct_messenger.dsuserver = ud.server
        self.direct_messenger.password = ud.password
        self.direct_messenger.username = ud.username
        path = pathlib.Path(filename + '.dsu')
        self._path = str(path)
        path.touch()
        msg = f"Online @{self.server} | {self.username}"
        self.footer.footer_label.configure(text=msg)
        self.profile.save_profile(path)
    
    def open_file(self):
        if self.status == True:
            self.body.reset_ui()
        filename = tk.filedialog.askopenfilename(filetypes=[('dsu', '*.dsu')])
        if filename == '':
            messagebox.showerror('ERROR!', 'No File Chosen.')
            return
        elif self.status == False:
            self.starter_frame.destroy()
            self.starter_frame1.destroy()
            self.welcome_msg.destroy()
            self.welcome_msg1.destroy()
            self.new_button.destroy()
            self.old_button.destroy()
            self.status = True
            self.main_program()
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
        msg = f"Online @{self.server} | {self.username}"
        self.footer.footer_label.configure(text=msg)

    def close(self):
        self.body.reset_ui()
        self.root.destroy()

    def main_program(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_file)
        menu_file.add_command(label='Open...', command=self.open_file)
        menu_file.add_command(label='Close', command=self.close)
        self.body = Body(self.root,
                        recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message,
                             con=self.configure_server, add=self.add_contact)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM) 

    def _draw(self):
        self.starter_frame = tk.Frame(master=self.root, bg='light blue')
        self.starter_frame.pack(side='top', fill="both", expand=True, padx=10, pady=10)
        self.starter_frame1 = tk.Frame(master=self.root, bg='light blue')
        self.starter_frame1.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)
        msg = '\n\nWelcome To DSP Messenger'
        msg_by = 'Created by: Steven Deng'
        self.welcome_msg = tk.Label(master=self.starter_frame, text=msg,
                               font='"Comic Sans MS" 20 normal', bg='light blue')
        self.welcome_msg1 = tk.Label(master=self.starter_frame, text=msg_by,
                                font='"Comic Sans MS" 14 normal', bg='light blue')
        self.welcome_msg.pack(fill='x', expand=True, anchor='s', side='top')
        self.welcome_msg1.pack(fill='x', expand=True, anchor='n')
        self.new_button = tk.Button(master=self.starter_frame1, text="New User",
                               width=20, command=self.new_file, padx=20, pady=20)
        self.new_button.pack(side=tk.LEFT, padx=30, pady=10, expand=True)
        self.old_button = tk.Button(master=self.starter_frame1, text="Registered User",
                               width=20, command=self.open_file, padx=20, pady=20)
        self.old_button.pack(side=tk.RIGHT, padx=30, pady=10, expand=True)

if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    app = MainApp(main)
    main.after(5000, app.check_new)
    main.mainloop()
