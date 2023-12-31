import customtkinter as ctk
from typing import Optional
from panels.panel import Panel
from panels.serial_panel import SerialEntryPanel
from panels.returned_panel import ReturnedPanel
from customtkinter import CTk, CTkButton, CTkFrame, CTkImage, CTkLabel
from PIL import Image
from config import *

PANEL_BUTTON_WIDTH = 250
PANEL_BUTTON_HEIGHT = 40

active_panel: Optional[Panel] = None

def handle_panel_shortcut(panel: Panel):
    global active_panel
    if active_panel is not None and active_panel != panel:
        stop_active_panel()
        start_panel(panel)
    if active_panel != panel:
        start_panel(panel)

def handle_enter_key():
    if active_panel is not None:
        if active_panel.main_frame.focus_get() == active_panel.serial_input.input._entry:
            active_panel.submit_serial()

def handle_save_sequence():
    if active_panel is not None and type(active_panel) is SerialEntryPanel:
        active_panel.submit_info()

def start_panel(panel: Panel):
    global active_panel
    home_panel.grid_forget()
    active_panel = panel
    active_panel.start()
    home_btn.place(relx=0.75, rely=0.9, bordermode="inside")

def stop_active_panel():
    global active_panel
    if active_panel is not None:
        active_panel.stop()
    active_panel = None
    
def return_home():
    #TODO CLEAR ALL DATA, ITEMS, ETC
    global active_panel
    stop_active_panel()
    home_panel.grid(column=0, row=1)
    home_btn.place_forget()

ctk.set_appearance_mode("dark")

# window
window = CTk()
window.title("Entry")
window.geometry("600x800")
background = window.cget("fg_color")

# content
main_frame = CTkFrame(master=window, bg_color=background, fg_color=background)
main_frame.pack()

print(iqlc_logo_path)
iqlc_logo = CTkImage(dark_image=Image.open(iqlc_logo_path), size=(350, 93)) #size=(245, 65))
logo_label = CTkLabel(master=main_frame, image=iqlc_logo, text="")
logo_label.grid(column=0, row=0)

# logo_label.place(bordermode="inside", rely=0.85, relx=0.01)

home_btn = CTkButton( fg_color=BUTTON_COLOR,
    master=window,
    text="חזור לדף הראשי",
    font=BUTTON_FONT,
    command=lambda: return_home()
)

home_panel = CTkFrame(main_frame, bg_color=background, fg_color=background)
home_panel.grid(column=0, row=1)
serial_entry_panel = SerialEntryPanel(main_frame)

serial_btn = CTkButton( fg_color=BUTTON_COLOR,
    master=home_panel,
    text="סריאלי",
    font=BUTTON_FONT,
    command=lambda: start_panel(serial_entry_panel),
    width=PANEL_BUTTON_WIDTH,
    height=PANEL_BUTTON_HEIGHT
)
serial_btn.pack(pady=60)

returned_panel = ReturnedPanel(main_frame)
returned_btn = CTkButton( fg_color=BUTTON_COLOR,
    master=home_panel,
    text="החזרות",
    font=BUTTON_FONT,
    command=lambda: start_panel(returned_panel),
    width=PANEL_BUTTON_WIDTH,
    height=PANEL_BUTTON_HEIGHT
)
returned_btn.pack()

key_binds = """               
קיצורי דרך


Enter  :חפש

Ctrl+1  :למסך סריאלי

Ctrl+2  :למסך החזרות

Ctrl+Shift+Q  :למסך הראשי

Ctrl+Shift+S  /  Ctrl+Enter  :עדכון מידע
"""

shortcuts = CTkLabel(
    master=home_panel,
    font=GENERAL_FONT,
    text=key_binds,
    justify="right",
    corner_radius=80,
    width=PANEL_BUTTON_WIDTH+20,
    bg_color=FORM_FRAME_COLOR
)
shortcuts.pack(pady=100)

#binds
window.bind('<Control-Key-1>', lambda event=None: handle_panel_shortcut(serial_entry_panel)) # go to serial
window.bind('<Control-Shift-Key-1>', lambda event=None: handle_panel_shortcut(serial_entry_panel))

window.bind('<Control-Key-2>', lambda event=None: handle_panel_shortcut(returned_panel)) # go to returned
window.bind('<Control-Shift-Key-2>', lambda event=None: handle_panel_shortcut(returned_panel))

window.bind('<Control-Q>', lambda event=None: return_home()) # back to home page

window.bind('<Return>', lambda event=None: handle_enter_key()) # search
window.bind('<Control-Shift-Return>', lambda event=None: handle_enter_key())

window.bind('<Control-S>', lambda event=None: handle_save_sequence()) # save
window.bind('<Control-Return>', lambda event=None: handle_save_sequence()) # 

window.mainloop()
