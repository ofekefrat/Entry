import customtkinter as ctk
from typing import Optional
from panels.panel import Panel
from panels.serial_panel import SerialEntryPanel
from panels.returned_panel import ReturnedPanel
from customtkinter import CTk, CTkButton, CTkFrame, CTkImage, CTkLabel
from PIL import Image
from config import *


active_panel: Optional[Panel] = None


def handle_enter_key():
    # print(self.main_frame.focus_get())
    # print(self.serial_input.input._entry)
    if active_panel is not None:
        if active_panel.main_frame.focus_get() == active_panel.serial_input.input._entry:
            active_panel.submit_serial()

def handle_save_sequence():
    if active_panel is not None:
        active_panel.submit_info()

def start_panel(panel: Panel):
    global active_panel
    home_panel.grid_forget()
    active_panel = panel
    active_panel.start()
    home_btn.place(relx=0.75, rely=0.9, bordermode="inside")
    
def return_home():
    #TODO CLEAR ALL DATA, ITEMS, ETC
    global active_panel
    if active_panel is not None:
        active_panel.stop()
    active_panel = None
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
    text="סריאלי (1)",
    font=BUTTON_FONT,
    command=lambda: start_panel(serial_entry_panel)
)
serial_btn.pack(pady=150)

returned_panel = ReturnedPanel(main_frame)
returned_btn = CTkButton( fg_color=BUTTON_COLOR,
    master=home_panel,
    text="החזרות (2)",
    font=BUTTON_FONT,
    command=lambda: start_panel(returned_panel)
)
returned_btn.pack()

#binds
# window.bind('<Control-1>', lambda event=None: start_panel(serial_entry_panel))
# window.bind('<Control-2>', lambda event=None: start_panel(returned_panel))
window.bind('<Control-Q>', lambda event=None: return_home())
window.bind('<Return>', lambda event=None: handle_enter_key())
window.bind('<Control-S>', lambda event=None: handle_save_sequence())
window.bind('<Control-Return>', lambda event=None: handle_save_sequence())

window.mainloop()
