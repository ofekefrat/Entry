from typing import Optional
from .panel import *
from customtkinter import CTk, CTkFrame, CTkButton
from excel_serial import Item
from config import *


class SerialEntryPanel(Panel):
    def __init__(self, root: CTk | CTkFrame):
        super().__init__(root, title="סריאלי")

        self.item = Optional[Item]

        # מספר סריאלי
        self.serial_input = DropListSearchBox(
            master=self.top_frame, row=1, label_text=":מספר סריאלי",

            btn_command=lambda: self.submit_serial(),
            value_list=SERIAL_BEGINNINGS,
        )

        self.form_frame = CTkFrame(self.main_frame, fg_color=FORM_FRAME_COLOR)
        self.form_frame.grid_columnconfigure(0, weight=2)

        # שם הזכאי
        self.name_input = TextBox(
            master=self.form_frame, row=0, label_text=":שם הזכאי"
        )

        # ת.ז
        self.id_input = TextBox(
            master=self.form_frame, row=1, label_text=":ת.ז"
        )

        # סוג המכשיר
        self.model_name_info = InfoBox(
            master=self.form_frame, row=2, label_text=":מכשיר"
        )
        self.model_name_info.hide()

        self.model_name_input = DroplistTextBox(
            master=self.form_frame, row=2, label_text=":מכשיר", values=WRITEABLE_MODELS,
        )
        self.model_name_input.hide()
        self.width = CTkComboBox(
            master=self.form_frame, width=60, font=GENERAL_FONT, values=["40", "42", "45", "48", "50"]
        )
        self.model_name_input.box.configure(command=lambda event=None: self.determine_show_width())
        self.width.set("")


        # תאריך אספקה
        self.delivery_date = DateBox(
            master=self.form_frame, row=3, label_text=":תאריך אספקה"
        )

        # זכאי קודם
        self.prev_name_info = InfoBox(
            master=self.form_frame, row=4, label_text=":שם הזכאי הקודם"
        )
        self.prev_name_info.hide()
        
        # כפתור שיגור
        self.info_submit_btn = CTkButton( fg_color=BUTTON_COLOR,
            master=self.form_frame,
            text="הוסף מידע",
            font=BUTTON_FONT,
            command=lambda: self.submit_info(),
        )

        # מוצר לא הוחזר
        self.not_returned_info = InfoBox(
            master=self.top_frame, row=2, label_column=3, label_text=NOT_RETURNED_EXCEPTION
        )
        self.not_returned_info.hide()

    def submit_serial(self):
        self.item = None

        self.form_frame.grid_forget()
        self.msg_label.grid_forget()
        self.prev_name_info.hide()
        self.model_name_input.hide()
        self.model_name_info.hide()
        self.not_returned_info.hide()
        self.width.grid_forget()
        self.width.set("")

        self.name_input.clear()
        self.id_input.clear()
        self.model_name_info.clear()
        self.model_name_input.clear()
        # self.delivery_date.clear()
        self.prev_name_info.clear()

        temp_item = Item(self.serial_input.get())

        if (
            isinstance(temp_item.wb, FileNotFoundError)
            or isinstance(temp_item.sheet, KeyError)
            or temp_item.row == -1
        ):
            self.show_msg(SERIAL_404)
            return

        if isinstance(temp_item.prev_name, AttributeError):
            self.show_msg(SERIAL_ROW_PROBLEM)
            return

        if not temp_item.is_new and not temp_item.is_returned:
            self.not_returned_info.set(temp_item.prev_name)
            self.not_returned_info.show()
            return

        self.form_frame.grid(row=1, column=0, pady=25)
        self.info_submit_btn.grid(row=5, column=1, pady=5)

        if temp_item.is_new:
            self.model_name_input.show()
        else:
            self.model_name_info.set(
                temp_item.model_name if type(temp_item.model_name) is str else NOT_FOUND
            )
            self.model_name_info.show()

            self.prev_name_info.set(
                temp_item.prev_name if type(temp_item.prev_name) is str else NOT_FOUND
            )
            self.prev_name_info.show()

        self.item = temp_item

    def submit_info(self):
        if isinstance(self.item, Item):
            try:
                success = self.item.update_info(
                    self.name_input.get(),
                    self.id_input.get(),
                    self.delivery_date.get().strftime("%d/%m/%y"),
                    f"{self.model_name_input.get()} {self.width.get()}",
                )
                if not success:
                    self.show_msg(FILE_UPDATED_UNEXPECTEDLY)
                    return
                else:
                    self.show_msg(FILE_UPDATE_SUCCESS, is_error=False)
                    self.info_submit_btn.grid_forget()
            except PermissionError:
                self.show_msg(SERIAL_FILE_IN_USE)

    def determine_show_width(self):
        if self.model_name_input.get() in WIDTH_REQUIRED:
            self.width.grid(row=2, column=0)
        else:
            self.width.grid_forget()
            self.width.set("")
