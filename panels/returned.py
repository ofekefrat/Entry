from customtkinter import *
from .panel import *
from config import *
from excel_serial import *

class ReturnedPanel(Panel):
    def __init__(self, root: CTk):
        super().__init__(root, title="דוח החזרות")
        
        #Frame content

        serial_input = DropListSearchBox(
            master=self.main_frame,
            row=1, column=0,
            label_text=":מספר סריאלי", 
            btn_command=lambda: self.submit_serial(serial_input.get()),
            value_list=serial_beginnings
        )
        serial_input.show()
        
        self.form_frame = CTkFrame(self.main_frame, fg_color=self.background)

        self.name_info = InfoBox(
            master=self.form_frame, row=0, column=0, label_text=":שם הזכאי"
        )
        self.name_info.show()
        
        self.model_name_info = InfoBox(
            master=self.form_frame, row=1, column=0, label_text=":מכשיר"
        )
        self.model_name_info.show()

        self.id_input = TextBox(
            master=self.form_frame, row=2, column=0, label_text=":ת.ז"
        )
        self.id_input.show()
        
    def submit_serial(self, input):
        self.item = None

        self.msg_label.grid_forget()
        
        self.clear_entry(self.name_info)
        self.clear_entry(self.id_input)

        temp_item = Item(input)

        if (
            isinstance(temp_item._wb, FileNotFoundError)
            or isinstance(temp_item.sheet, KeyError)
            or temp_item.row == -1
        ):
            self.show_msg("מספר סריאלי לא נמצא", is_error=True)
            return

        if isinstance(temp_item.prev_name, AttributeError):
            self.show_msg("נראה כי יש בעיה עם השורה המתבקשת. אנא בדקו אותה בקובץ הסריאלי", is_error=True)
            return

        if not temp_item.is_returned:
            self.show_msg("המוצר המבוקש לא הוחזר או טרם הונפק", is_error=True)

        self.form_frame.grid(row=2, column=0)

        self.item = temp_item