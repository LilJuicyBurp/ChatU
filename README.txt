My messenger program functions through 5 modules. a5 calls A5_gui and starts the gui mainloop then the other three modules
Profile, ds_messenger, and ds_protocol are called in the A5_gui module. 

The only function in ds_protocol is directmessage and is used to decipher the jason return from the DSP server.

The ds_messenger module has the directmessage and DirectMessenger classes. The fromer is used to store messages and their
specified data. The Latter contains all the methods to communicate with the DSP server such as connecting sending and
retrieving data.

The Profile module contains the profile class which stores data about the user's profile while the program runs and contains
methods for local storage and data extraction.

The most important module is the a5_gui module and there are four classes. First is Body, which contains all the methods 
responsible for the body part of the gui which is the message box, chat box, and friends list. Next the Footer class
performs the same responsiblities for the gui footer as the body class did for the body. Next is the NewContactDialog class
which is an extra window that I utilize when prompting the user for data to create or modify a profile. The mainapp class 
has the traceback methods for the footer and body. It also contains methods that correspond to each menu option.

BREAK DOWN OF MY MESSENGER:
1. There is a start menu which prompts the user to create a profile or load an existing one.
2. After my main menu will be printed. At this time all the bottons and chat boxes are disabled
3. When the user clicks on a contact in treeview, the chat history will display and all buttons will bve enabled
4. My program also looks for new messages every 5 seconds. 
5. The file menu contains options to create a new user, open a existing user, or quit the program.
NOTEWORTHY FEATURES:
1. My code keeps track of messages that remain in the message box when the user switches between contacts
2. I have alot of custom message boxes that come up to notify the user when something doesn't happen. For example, if someone
changes their username to empty spaces the operation won't be processed. The same happens when some doesn't enter enough 
info when creating a user or adding a contact.
3. The chat history is in printed in reverse to mimic model IM software in that you scroll up to view previous messages and
not down.
4. When someone who isn't friended sends you a message they will be added to the contact list automatically.
5. The bottom left corner contains the users name and the server that they are on.
6. When clicking the new user and open user buttons the loaded user will be logged out and the gui will be reset.