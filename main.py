import customtkinter as ctk
from panels.panel import Panel
from panels.serial_entry import SerialEntryPanel
from panels.returned import ReturnedPanel
from customtkinter import CTk, CTkButton, CTkFrame
from config import *

active_panel: Panel = None # type: ignore

def start_panel(panel: Panel):
    global active_panel
    home_panel.pack_forget()
    active_panel = panel
    active_panel.start()
    home_btn.place(relx=0.75, rely=0.9, bordermode="inside")
    
def return_home():
    active_panel.stop()
    home_panel.pack()
    home_btn.place_forget()
    # CLEAR ALL DATA, ITEMS, ETC

ctk.set_appearance_mode("light")

# window
window = CTk()
window.title("Entry")
window.geometry("600x600")
background = window.cget("fg_color")


# content
home_btn = CTkButton(
    window,
    text="חזור לדף הראשי",
    font=BUTTON_FONT,
    command=lambda: return_home()
)

home_panel = CTkFrame(window, bg_color=background, fg_color=background)
home_panel.pack()
serial_entry_panel = SerialEntryPanel(window)
serial_entry_btn = CTkButton(
    home_panel,
    text="סריאלי",
    font=BUTTON_FONT,
    command=lambda: start_panel(serial_entry_panel)
)
serial_entry_btn.pack(pady=150)

returned_panel = ReturnedPanel(window)
returned_btn = CTkButton(
    home_panel,
    text="החזרות",
    font=BUTTON_FONT,
    command=lambda: start_panel(returned_panel)
)
returned_btn.pack()

window.mainloop()
