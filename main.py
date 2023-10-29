import customtkinter as ctk
from tkcalendar import DateEntry
from interaction import *
from customtkinter import *

ctk.set_appearance_mode("light")


# window
background = "#EAEAEA"
window = CTk()
window.title("Entry")
window.geometry("600x600")
generalFont = CTkFont("arial", 15)
btnFont = CTkFont("arial", 17)
infoFont = CTkFont("arial bold", 17)


#   content
main_frame = CTkFrame(window, bg_color=background, fg_color=background)
main_frame.pack()

msg_label = CTkLabel(main_frame, text_color="white", font=generalFont, corner_radius=5)

controller = Controller(msg_label)


# title
title = CTkLabel(
    main_frame,
    text="הכנסת נתונים",
    font=CTkFont("arial", 23, underline=True),
    bg_color=background,
)
title.grid(row=0, column=1, pady=5)


# serial
serial_frame = CTkFrame(main_frame, fg_color=background)
serial_frame.grid(row=1, column=1, pady=5)

serial_label = CTkLabel(
    serial_frame, text="  :מס' סריאלי ", font=generalFont, bg_color=background
)
serial_label.grid(row=0, column=3)

serial_input = CTkEntry(serial_frame, bg_color=background, font=generalFont)
serial_input.grid(row=0, column=2, padx=10)

serial_droplist = CTkOptionMenu(
    serial_frame,
    bg_color=background,
    fg_color="white",
    button_color="white",
    button_hover_color="gray",
    font=generalFont,
    text_color="black",
    anchor="e",
    width=20,
    values=["2400-03-", "2400-24-", "N220", "N160", "N50", "N60"],
)
serial_droplist.grid(row=0, column=1)

serial_sumbit_btn = CTkButton(
    main_frame,
    text="חיפוש",
    width=10,
    font=btnFont,
    bg_color=background,
    command=lambda: controller.submit_serial(
        serial_droplist.get() + serial_input.get(),
        form_frame,
        name_input,
        id_input,
        newModel_input,
        newModel_frame,
        existingModel_frame,
        existingModel_Name,
        prev_name,
        prev_name_label,
        deviceBirthday_date,
        info_submit_btn,
        deviceReturn_frame,
        deviceReturn_name,
    ),
)
serial_sumbit_btn.grid(row=1, column=0, padx=15)


#   form
# name
form_frame = CTkFrame(main_frame, fg_color=background)

name_label = CTkLabel(form_frame, text="  :שם", font=generalFont, bg_color=background)
name_label.grid(row=0, column=3, pady=5)

name_input = CTkEntry(
    form_frame, bg_color=background, font=generalFont, justify="right"
)
name_input.grid(row=0, column=2, padx=10, pady=5)


# previous name
prev_name_label = CTkLabel(
    form_frame, text=":זכאי קודם", font=generalFont, bg_color=background
)
prev_name = CTkLabel(form_frame, bg_color=background, font=infoFont, justify="right")


# id
id_label = CTkLabel(form_frame, text=":מס' זהות", font=generalFont, bg_color=background)
id_label.grid(row=1, column=3, pady=5)

id_input = CTkEntry(form_frame, bg_color=background, font=generalFont)
id_input.grid(row=1, column=2, padx=10, pady=5)


# date
date_label = CTkLabel(
    form_frame, text=":מועד אספקה", font=generalFont, bg_color=background
)
date_label.grid(row=3, column=3, pady=5)

date_input = DateEntry(form_frame, date_pattern="dd/mm/yy")
date_input.grid(row=3, column=2, padx=10, pady=5)


#   model frames
# new model
newModel_frame = CTkFrame(main_frame, fg_color=background)
newModel_label = CTkLabel(
    newModel_frame, text="       :דגם      ", font=generalFont, bg_color=background
)
newModel_label.grid(row=0, column=1)

newModel_input = CTkEntry(newModel_frame, bg_color=background, font=generalFont)
newModel_input.grid(row=0, column=0, padx=10)


# existing model
existingModel_frame = CTkFrame(main_frame, fg_color=background)
existingModel_label = CTkLabel(
    existingModel_frame, text="       :דגם      ", font=generalFont, bg_color=background
)
existingModel_label.grid(row=0, column=1)

existingModel_Name = CTkLabel(existingModel_frame, bg_color=background, font=infoFont)
existingModel_Name.grid(row=0, column=0, padx=10)

deviceBirthday_label = CTkLabel(
    existingModel_frame, bg_color=background, font=generalFont, text=":תאריך הנפקת מוצר"
)
deviceBirthday_label.grid(row=1, column=1, padx=10)

deviceBirthday_date = CTkLabel(existingModel_frame, bg_color=background, font=infoFont)
deviceBirthday_date.grid(row=1, column=0, padx=10)

info_submit_btn = CTkButton(
    main_frame,
    bg_color=background,
    text="הוסף מידע",
    font=CTkFont("arial", 17),
    command=lambda: controller.submit_info(
        name_input.get(), id_input.get(), date_input.get_date(), newModel_input
    ),
)


# return
deviceReturn_frame = CTkFrame(main_frame, fg_color=background)
deviceReturn_label = CTkLabel(
    deviceReturn_frame,
    bg_color=background,
    font=generalFont,
    text=" :המוצר לא הוחזר מזכאי קודם",
)
deviceReturn_label.grid(row=0, column=2)
deviceReturn_name = CTkLabel(deviceReturn_frame, bg_color=background, font=infoFont)
deviceReturn_name.grid(row=0, column=1, padx=10)

deviceReturn_btn = CTkButton(
    deviceReturn_frame,
    bg_color=background,
    text="סמן הוחזר",
    font=btnFont,
    command=lambda: controller.submit_returned(),
)
deviceReturn_btn.grid(row=0, column=0, padx=10)


window.mainloop()
