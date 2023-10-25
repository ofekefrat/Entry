import customtkinter as ctk
from customtkinter import *
from tkcalendar import DateEntry
from serial_module import Item

item = None

def submit_serial(input,
                  formFrame: CTkFrame,
                  newModelFrame: CTkFrame,
                  existingModelFrame: CTkFrame,
                  existingModelName: CTkLabel,
                  prevName: CTkLabel,
                  prevNameLabel: CTkLabel):
    global item
    item = None

    msg_label.grid_forget()
    existingModelFrame.grid_forget()
    newModelFrame.grid_forget()
    prevName.grid_forget()
    prevNameLabel.grid_forget()
    formFrame.grid_forget()


    tempItem = Item(input)

    if isinstance(tempItem.wb, FileNotFoundError) or isinstance(tempItem.sheet, KeyError):
        show_msg("מספר סריאלי לא קיים", error=True)
        return
    
    if tempItem.column == -1:
        show_msg("המוצר לא הוחזר", error=True)
        return
    
    form_frame.grid(row=2, column=1, pady=5)

    if tempItem.new:
        newModelFrame.grid(row=3, column=1, pady=5)
    else:
        existingModelFrame.grid(row=3, column=1, pady=5) 
        existingModelName.configure(text=tempItem.modelName)

        prevNameLabel.grid(row=0, column=1, pady=5, padx=(0, 20))
        prevName.grid(row=0, column=0, padx=10, pady=5)
        prevName.configure(text=tempItem.prevName)

    info_submit.grid(row=4, column=1, pady=5)
    item = tempItem


def submit_info(name, id, date, modelEntry: CTkEntry):
    global item
    model = modelEntry.get()
    date = date.strftime("%d/%m/%y")
    try:
        item.update_info(name, id, date, model)
        show_msg("הקובץ עודכן בהצלחה", error=False)
    except PermissionError:
        show_msg("הקובץ המתבקש נמצא בשימוש, אנא דאג לסגירתו", error=True)

def show_msg(description, error):
    global msg_label
    msg_label.configure(text=description)
    if error:
        msg_label.configure(bg_color="red")
    else:
        msg_label.configure(bg_color="green")
    msg_label.grid(row=5, column=1)
            
ctk.set_appearance_mode("light")
#window
background = "#EAEAEA"
window = CTk()
window.title("Injector")
window.geometry("600x600")
globalFont = CTkFont("arial", 15)
main_frame = CTkFrame(window, bg_color=background, fg_color=background)
main_frame.pack()

#title
title = CTkLabel(main_frame,
    text="הכנסת נתונים",
    font=CTkFont("arial", 23, underline=True),
    bg_color=background
)
title.grid(row=0, column=1, pady=5)

#serial
serial_frame = CTkFrame(main_frame, fg_color=background)
serial_frame.grid(row=1, column=1, pady=5)

serial_label = CTkLabel(serial_frame,
    text="  :מס' סריאלי ",
    font=globalFont,
    bg_color=background
)
serial_label.grid(row=0, column=2)

serial_input = CTkEntry(serial_frame, bg_color=background)
serial_input.grid(row=0, column=1, padx=10)

serial_sumbit = CTkButton(main_frame,
    text = "חפש",
    width = 10,
    font = globalFont,
    bg_color = background,
    command = lambda: submit_serial(serial_input.get(),
                                    form_frame,
                                    newModel_frame,
                                    existingModel_frame,
                                    existingModel_Name,
                                    prev_name,
                                    prev_name_label)
)
serial_sumbit.grid(row=1, column=0, pady=5)


#   form
#name
form_frame = CTkFrame(main_frame, fg_color=background)

name_label = CTkLabel(form_frame,
    text="  :שם",
    font=globalFont,
    bg_color=background
)
name_label.grid(row=0, column=3, pady=5)

name_input = CTkEntry(form_frame, bg_color=background, justify = "right")
name_input.grid(row=0, column=2, padx=10, pady=5)

#previous name --------------------------
prev_name_label = CTkLabel(form_frame,
    text=":זכאי קודם",
    font=globalFont,
    bg_color=background
)

prev_name = CTkLabel(form_frame, bg_color=background, justify = "right")

#id
id_label = CTkLabel(form_frame,
    text=":מס' זהות",
    font=globalFont, 
    bg_color=background
)
id_label.grid(row=1, column=3, pady=5)

id_input = CTkEntry(form_frame, bg_color=background)
id_input.grid(row=1, column=2, padx=10, pady=5)

#date
date_label = CTkLabel(form_frame,
    text=":מועד אספקה",
    font=globalFont,
    bg_color=background
)
date_label.grid(row=3, column=3, pady=5)

# date_entry = CTkEntry(form_frame, bg_color=background)
date_input = DateEntry(form_frame, )
date_input.grid(row=3, column=2, padx=10, pady=5)

#   model frames
#new model
newModel_frame = CTkFrame(main_frame, fg_color=background)
newModel_label = CTkLabel(newModel_frame,
    text="       :דגם      ",
    font=globalFont,
    bg_color=background
)
newModel_label.grid(row=0, column=1)

newModel_input = CTkEntry(newModel_frame, bg_color=background)
newModel_input.grid(row=0, column=0, padx=10)

#existing model
existingModel_frame = CTkFrame(main_frame, fg_color=background)
existingModel_label = CTkLabel(existingModel_frame,
    text="       :דגם      ",
    font=globalFont,
    bg_color=background
)
existingModel_label.grid(row=0, column=1)

existingModel_Name = CTkLabel(existingModel_frame, bg_color=background)
existingModel_Name.grid(row=0, column=0, padx=10)

info_submit = CTkButton(main_frame, bg_color=background,
    text = "הוסף מידע",
    font = CTkFont("arial", 17),
    command = lambda: submit_info(name_input.get(),
                                  id_input.get(),
                                  date_input.get_date(),
                                  newModel_input)
)

msg_label = CTkLabel(main_frame, text_color="white", font=globalFont, corner_radius=5)

window.mainloop()