import customtkinter
from tkinter import filedialog
import threading
import time
import os
import random
from CTkMenuBarPlus import *
import configparser

config = configparser.ConfigParser()
config.read("Program Files/Config.ini")

# button start stop
BSS = False
Theme = 0

WindowWidth = 600
WindowHeight = 500

# this loads light and dark theme control
ModesDefaultTheme = config.get("TextSwitcher", "Theme",)

    
# this sets up the Window
customtkinter.set_appearance_mode(ModesDefaultTheme)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

Window = customtkinter.CTk()

ScreenWidth = Window.winfo_screenwidth()
ScreenHeight = Window.winfo_screenheight()

X = (ScreenWidth / 2) - (WindowWidth / 2)
Y = (ScreenHeight / 2) - (WindowHeight / 2)

Window.title("BATS")
Window.iconbitmap(os.path.join("Program Files", "images", "Barely Adequate Text Switcher.Ico"))
Window.geometry(f"{WindowWidth}x{WindowHeight}+{int(X)}+{int(Y)}")

def ChangeTheme(): # light and dark theme control
    config.set("TextSwitcher", "Theme", Theme)
    with open(os.path.join("Program Files", "Config.ini"), "w") as configfile:
        config.write(configfile)
        
    customtkinter.set_appearance_mode(Theme)



def OpenFile(): # this opens and loads the selected file
    File = filedialog.askopenfile(parent=Window, initialdir=os.path.join("You're Saved Files"), filetypes=[("Text Files", "*.txt")],)
    if File:
        TextSwitcherTextBox.delete(0.0, "end")
        TextSwitcherTextBox.insert(0.0, File.read())

def SaveFile(): # this saves the text currently in the Text box
    File = filedialog.asksaveasfilename(parent=Window, defaultextension=".*", filetypes=[("Text Files", "*.txt")], initialdir=os.path.join("You're Saved Files"))
    if File:
        with open (File, "w") as TheFile:
            TheFile.write(str(TextSwitcherTextBox.get(1.0, "end")[:-1]))



# sets up the Menu Bar
MenuBar = CTkMenuBar(master=Window)

FileMenu = MenuBar.add_cascade("File")
OptionsButton = MenuBar.add_cascade("Options")

FileMenu = CustomDropdownMenu(widget=FileMenu)
FileMenu.add_option(option="Open File", command=OpenFile)
FileMenu.add_option(option="Save File", command=SaveFile)


# light and dark theme menu
ThemeMenu = CustomDropdownMenu(widget=OptionsButton)
ThemeSubmenu = ThemeMenu.add_submenu("Theme")
ThemeSubmenu.add_option(option="System Default", command=lambda: (globals().update(Theme = "system"),ChangeTheme()))
ThemeSubmenu.add_option(option="Light", command=lambda: (globals().update(Theme = "light"), ChangeTheme()))
ThemeSubmenu.add_option(option="Dark", command=lambda: (globals().update(Theme = "dark"), ChangeTheme()))


# sets up the frame holding the tabs
Frame = customtkinter.CTkFrame(Window, width=WindowWidth + 50, height=WindowHeight + 50, fg_color="transparent")
Frame.pack(padx=0, pady=0)

# this sets up the Tabs
tabview = customtkinter.CTkTabview(Frame, width=WindowWidth - 50, height=WindowHeight - 60, corner_radius=2, fg_color="transparent")
tabview.pack(padx=20, pady=5)

tab_1 = tabview.add("Text Switcher")
#tab_2 = tabview.add("tab 2")
tabview.set("Text Switcher")  # set currently visible tab


        
def DefaultText(): # this Sets current text in the text box as default
    with open(os.path.join("Program Files", "Line Change Save File.txt"), "w") as File:
        File.write(TextSwitcherTextBox.get(0.0, "end")[:-1])
        
    if SecondsBetweenSwitchEntry.get() == "":
        SecondsBetweenSwitchEntry.insert(0, int(1))
        
    config.set("TextSwitcher", "secondsbetween", SecondsBetweenSwitchEntry.get())
    with open(os.path.join("Program Files", "Config.ini"), "w") as configfile:
        config.write(configfile)
        
    config.set("TextSwitcher", "randomonoff", RandomCheckBox.get())
    with open(os.path.join("Program Files", "Config.ini"), "w") as configfile:
        config.write(configfile)


# this sets up the Default Text Button
buttonDefaultText = customtkinter.CTkButton(master=tab_1, text="Set as default text",command=DefaultText,)
buttonDefaultText.place(relx = 0.84, rely = 0.95, relwidth=0.25, anchor="center")


# sets up the frame holding the Entry Box on Text Switcher Tab
SecondFrameTab1 = customtkinter.CTkFrame(master=tab_1, width=WindowWidth - 80, height=200, fg_color="transparent")
SecondFrameTab1.pack(padx=2, pady=5)

# this sets up the Text box
TextSwitcherTextBox = customtkinter.CTkTextbox(master=SecondFrameTab1, wrap="none", font=("Arial", 17))
TextSwitcherTextBox.place(relx = 0.5, rely = 0.5, relwidth=0.6, anchor="center")


def validate_entry(text): # forces the input of the Input Box to be decimal
    return text.isdecimal()

# this sets up the top label for the seconds input
SwitchLineEveryLabelTop = customtkinter.CTkLabel(master=SecondFrameTab1, text="Switch\nText Every")
SwitchLineEveryLabelTop.place(relx = 0.08, rely = 0.13, relwidth=0.12, anchor="center")

# this sets up the Bottom label for the seconds input
SwitchLineEveryLabelBottom = customtkinter.CTkLabel(master=SecondFrameTab1, text="Seconds")
SwitchLineEveryLabelBottom.place(relx = 0.08, rely = 0.43, relwidth=0.12, anchor="center")

# creates the entry box for inputting the number of seconds between text switching
SecondsBetweenSwitchEntry = customtkinter.CTkEntry(master=SecondFrameTab1, validate="key", validatecommand=(SecondFrameTab1.register(validate_entry), "%S"), placeholder_text="Input Seconds")
SecondsBetweenSwitchEntry.place(relx = 0.08, rely = 0.3, relwidth=0.12, anchor="center")


# this loads default number of seconds between text switching
SecondsBetweenSwitchEntry.insert(0, str(config.get("TextSwitcher", "secondsbetween",)))

# this loads default text into text box
with open(os.path.join("Program Files", "Line Change Save File.txt"), "r") as TextSwitcherTextBoxSave:
    TextSwitcherTextBox.insert(0.0, TextSwitcherTextBoxSave.read())


def LineChange(): # this is the text switching logic that runs on another thread
    global BSS
    Lines = TextSwitcherTextBox.get("0.0", "end").count('\n')
    UnsplitText = TextSwitcherTextBox.get("0.0", "end")
    InputSeconds = SecondsBetweenSwitchEntry.get()
    if InputSeconds == "" or InputSeconds[0:1] == "0":
        SecondsBetweenSwitchEntry.delete(0, len(InputSeconds))
        SecondsBetweenSwitchEntry.insert(0, int(1))
        InputSeconds = int(1)

    while BSS:
        RandomOrder = random.sample(range(0, Lines), Lines)
        time.sleep(0.1)
        for Line in range(0, Lines):
            with open(os.path.join("Switcher Files", "Text Switcher.txt"), "w") as txtSwitcher:
                
                if RandomCheckBoxState.get() == "off":
                    txtSwitcher.write(UnsplitText.splitlines()[Line])
                else:txtSwitcher.write(UnsplitText.splitlines()[RandomOrder[int(Line)]])
                
            for seconds in range(0, int(InputSeconds)):
                if BSS == False:
                    break
                
                time.sleep(1)
        if BSS == False:
            with open(os.path.join("Switcher Files", "Text Switcher.txt"), "w") as txtSwitcher:
                txtSwitcher.write(UnsplitText.splitlines()[0])
            # this is necessary to Kill the thread
            break

def StartStop_event(): # turns a button into a toggle
    global BSS
    if BSS == False:
       BSS = True
       ButtonStartStop.configure(text=("Stop"), fg_color="#DB280B", hover_color="dark red")
       # creates and starts the thread
       LineChangeThread = threading.Thread(target=LineChange, daemon=True)
       LineChangeThread.start()           
           
    elif BSS == True:
       BSS = False
       ButtonStartStop.configure(text=("Start"), fg_color="green", hover_color="dark green")
        
# this loads random function default state
RandomCheckBoxState = customtkinter.StringVar(value=config.get("TextSwitcher", "randomonoff",))

# This is the checkbox for a random sequence
RandomCheckBox = customtkinter.CTkCheckBox(master=tab_1, text="Random\nSequence", variable=RandomCheckBoxState, onvalue="on", offvalue="off")
RandomCheckBox.place(relx = 0.13, rely = 0.74, relwidth=0.2, anchor="center")

# this sets up the Start/Stop Button
ButtonStartStop = customtkinter.CTkButton(tab_1, text=("Start"), font=("Arial", 18), command=StartStop_event, fg_color="green", hover_color="dark green")
ButtonStartStop.pack(pady=10)


Window.mainloop()