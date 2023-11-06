from .panel import Panel
from customtkinter import *
from tkcalendar import DateEntry
from excel_serial import Item
from config import *

class SerialEntryPanel(Panel):
    def __init__(self, root: CTk):
        super().__init__(root, title="סריאלי")

        # Frame content

        # serial
        self.serial_frame = CTkFrame(self.main_frame, fg_color=self.background)
        self.serial_frame.grid(row=1, column=1, pady=5)

        serial_label = CTkLabel(
            self.serial_frame, text="  :מס' סריאלי ", font=general_font, bg_color=self.background
        )
        serial_label.grid(row=0, column=3)

        serial_input = CTkEntry(self.serial_frame, bg_color=self.background, font=general_font)
        serial_input.grid(row=0, column=2, padx=10)

        serial_droplist = CTkOptionMenu(
            self.serial_frame,
            bg_color=self.background,
            fg_color="white",
            button_color="white",
            button_hover_color="gray",
            font=general_font,
            text_color="black",
            anchor="e",
            width=20,
            values=serial_beginnings
        )
        serial_droplist.grid(row=0, column=1)

        serial_sumbit_btn = CTkButton(
            self.main_frame,
            text="חיפוש",
            width=10,
            font=btn_font,
            bg_color=self.background,
            command=lambda: self.submit_serial(
                serial_droplist.get() + serial_input.get()
            )
        )
        serial_sumbit_btn.grid(row=1, column=0, padx=15)


        #   form
        # name
        self.form_frame = CTkFrame(self.main_frame, fg_color=self.background)

        name_label = CTkLabel(self.form_frame, text="  :שם", font=general_font, bg_color=self.background)
        name_label.grid(row=0, column=3, pady=5)

        self.name_input = CTkEntry(
            self.form_frame, bg_color=self.background, font=general_font, justify="right"
        )
        self.name_input.grid(row=0, column=2, padx=10, pady=5)


        # previous name
        self.prev_name_label = CTkLabel(
            self.form_frame, text=":זכאי קודם", font=general_font, bg_color=self.background
        )
        self.prev_name = CTkLabel(self.form_frame, bg_color=self.background, font=info_font, justify="right")


        # id
        id_label = CTkLabel(self.form_frame, text=":מס' זהות", font=general_font, bg_color=self.background)
        id_label.grid(row=1, column=3, pady=5)

        self.id_input = CTkEntry(self.form_frame, bg_color=self.background, font=general_font)
        self.id_input.grid(row=1, column=2, padx=10, pady=5)


        # date
        date_label = CTkLabel(
            self.form_frame, text=":מועד אספקה", font=general_font, bg_color=self.background
        )
        date_label.grid(row=3, column=3, pady=5)

        self.date_input = DateEntry(self.form_frame, date_pattern="dd/mm/yy")
        self.date_input.grid(row=3, column=2, padx=10, pady=5)


        #   model frames
        # new model
        self.new_model_frame = CTkFrame(self.main_frame, fg_color=self.background)
        new_model_label = CTkLabel(
            self.new_model_frame, text="       :דגם      ", font=general_font, bg_color=self.background
        )
        new_model_label.grid(row=0, column=1)

        self.new_model_input = CTkEntry(self.new_model_frame, bg_color=self.background, font=general_font)
        self.new_model_input.grid(row=0, column=0, padx=10)


        # existing model
        self.existing_model_frame = CTkFrame(self.main_frame, fg_color=self.background)
        existing_model_label = CTkLabel(
            self.existing_model_frame, text="       :דגם      ", font=general_font, bg_color=self.background
        )
        existing_model_label.grid(row=0, column=1)

        self.existing_model_Name = CTkLabel(self.existing_model_frame, bg_color=self.background, font=info_font)
        self.existing_model_Name.grid(row=0, column=0, padx=10)

        device_birthday_label = CTkLabel(
            self.existing_model_frame, bg_color=self.background, font=general_font, text=":תאריך הנפקת מוצר"
        )
        device_birthday_label.grid(row=1, column=1, padx=10)

        self.device_birthday_date = CTkLabel(self.existing_model_frame, bg_color=self.background, font=info_font)
        self.device_birthday_date.grid(row=1, column=0, padx=10)

        self.info_submit_btn = CTkButton(
            self.main_frame,
            bg_color=self.background,
            text="הוסף מידע",
            font=btn_font,
            command=lambda: self.submit_info()
        )

        # return
        self.device_return_frame = CTkFrame(self.main_frame, fg_color=self.background)
        device_return_label = CTkLabel(
            self.device_return_frame,
            bg_color=self.background,
            font=general_font,
            text=" :המוצר לא הוחזר מזכאי קודם",
        )
        device_return_label.grid(row=0, column=2)
        self.device_return_name = CTkLabel(self.device_return_frame, bg_color=self.background, font=info_font)
        self.device_return_name.grid(row=0, column=1, padx=10)

    def submit_serial(self, input):
        self.item = None

        self.msg_label.grid_forget()
        self.existing_model_frame.grid_forget()
        self.new_model_frame.grid_forget()
        self.prev_name.grid_forget()
        self.prev_name_label.grid_forget()
        self.form_frame.grid_forget()
        self.info_submit_btn.grid_forget()
        self.device_return_frame.grid_forget()

        self.clear_entry(self.name_input)
        self.clear_entry(self.id_input)
        self.clear_entry(self.new_model_input)

        tempItem = Item(input)

        if (
            isinstance(tempItem._wb, FileNotFoundError)
            or isinstance(tempItem.sheet, KeyError)
            or tempItem.row == -1
        ):
            self.show_msg("מספר סריאלי לא נמצא", is_error=True)
            return

        if isinstance(tempItem.prev_name, AttributeError):
            self.show_msg("נראה כי יש בעיה עם השורה המתבקשת. אנא בדקו אותה בקובץ הסריאלי", is_error=True)
            return

        if tempItem.is_returned or tempItem.is_new:
            self.form_frame.grid(row=2, column=1, pady=5)
            self.info_submit_btn.grid(row=4, column=1, pady=5)

        if tempItem.is_new:
            self.new_model_frame.grid(row=3, column=1, pady=5)
        else:
            self.existing_model_frame.grid(row=3, column=1, pady=5)
            self.existing_model_Name.configure(text=tempItem.model_name)
            self.device_birthday_date.configure(text=tempItem.device_birthday)

            if tempItem.is_returned:
                self.prev_name_label.grid(row=0, column=1, pady=5, padx=(0, 20))
                self.prev_name.grid(row=0, column=0, padx=10, pady=5)
                self.prev_name.configure(text=tempItem.prev_name)
            else:
                self.device_return_frame.grid(row=4, column=1, pady=5)
                self.device_return_name.configure(text=tempItem.prev_name)

        self.item = tempItem

    def submit_info(self):
        try:
            success = self.item._update_info(
                self.name_input.get(),
                self.id_input.get(),
                self.date_input.get_date().strftime("%d/%m/%y"),
                self.new_model_input.get()
                )
            if not success:
                self.show_msg(
                    'השורה עודכנה ע"י משתמש אחר. אנא הקש "חיפוש" שנית', is_error=True
                )
                return
            else:
                self.show_msg("הקובץ עודכן בהצלחה", is_error=False)
                self.info_submit_btn.grid_forget()
        except PermissionError:
            self.show_msg("הקובץ המתבקש נמצא בשימוש, אנא דאג לסגירתו", is_error=True)

    def submit_returned(self):
        try:
            success = self.item._set_returned()
            if not success:
                self.show_msg(
                    'השורה עודכנה ע"י משתמש אחר. אנא הקש "חיפוש" שנית', is_error=True
                )
            else:
                self.show_msg("הקובץ עודכן בהצלחה", is_error=False)
        except PermissionError:
            self.show_msg("הקובץ המתבקש נמצא בשימוש, אנא דאג לסגירתו", is_error=True)

