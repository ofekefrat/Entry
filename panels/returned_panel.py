from _pydatetime import date
from excel_record import update_record
from .panel import *
from config import *
from excel_serial import Item


class ReturnedPanel(Panel):
    def __init__(self, root: CTk | CTkFrame):
        super().__init__(root, title="דוח החזרות")

        #מספר סריאלי
        self.serial_input = DropListSearchBox(
            master=self.top_frame, row=1, label_text=":מספר סריאלי",
            btn_command=lambda: self.submit_serial(self.serial_input.get()),
            value_list=SERIAL_BEGINNINGS
        )

        self.form_frame = CTkFrame(self.main_frame, fg_color=FORM_FRAME_COLOR)

        #שם הזכאי
        self.name_info = InfoBox(
            master=self.form_frame, row=0, label_text=":שם הזכאי"
        )

        #ת.ז
        self.id_input = TextBox(
            master=self.form_frame, row=1, label_text=":ת.ז"
        )

        #לשכה
        self.department_input = DroplistTextBox(
            master=self.form_frame, row=2, label_text=":לשכה", values=MOH_DEPARTMENTS
        )

        #מספר בקשה
        self.request_number_input = TextBox(
            master=self.form_frame, row=3, label_text=":מספר בקשה"
        )

        #סוג המכשיר
        self.model_name_info = InfoBox(
            master=self.form_frame, row=4, label_text=":מכשיר"
        )

        #תאריך קבלת פנייה
        self.call_recieved_date = DateBox(
            master=self.form_frame, row=5, label_text=":תאריך קבלת פנייה לאיסוף"
        )

        #תאריך ביצוע
        self.collection_date = DateBox(
            master=self.form_frame, row=6, label_text=":תאריך ביצוע איסוף"
        )

        #נמסרה הודעה ללשכה
        self.moh_notify_date = DateBox(
            master=self.form_frame, row=7, label_text=":תאריך מסירת הודעה ללשכה"
        )
        
        #תאריך אספקה מקורי
        self.initial_issuing_info = InfoBox(
            master=self.form_frame, row=8, label_text=":תאריך אספקה מקורי"
        )

        #כפתור שיגור
        self.info_submit_btn = CTkButton( fg_color=BUTTON_COLOR,
            master=self.form_frame,
            bg_color=self.background,
            text="הוסף מידע",
            font=BUTTON_FONT,
            command=lambda: self.submit_info({
                "name": self.name_info.get(),
                "id": self.id_input.get(),
                "department": self.department_input.get(),
                "request" : self.request_number_input.get(),
                "model": self.model_name_info.get(),
                "serial": self.serial_input.get(),
                "call_recieved": self.call_recieved_date.get(),
                "collection_date": self.collection_date.get(),
                "moh_nofitied_date": self.moh_notify_date.get(),
                "initial_issuing_date": self.initial_issuing_info.get()
            })
        )

        #כפתור סימון בלבד (למקרה של קובץ סריאלי פתוח)
        self.only_set_returned_btn = CTkButton( fg_color=BUTTON_COLOR,
            master=self.form_frame,
            bg_color=self.background,
            text="סמן כהוחזר",
            font=BUTTON_FONT,
            command=lambda: self.panel_set_returned()
        )

        #מוצר כבר הוחזר
        self.already_returned_info = InfoBox(
            master=self.top_frame, row=2, label_column=2, label_text=ALREADY_RETURNED_EXCEPTION
        )
        self.already_returned_info.hide()
        
    def submit_serial(self, input):
        self.item = None
        
        self.already_returned_info.hide()
        self.only_set_returned_btn.grid_forget()
        self.form_frame.grid_forget()
        self.msg_label.grid_forget()
        self.name_info.clear()
        self.id_input.clear()
        self.department_input.clear()
        self.request_number_input.clear()
        self.model_name_info.clear()
        # self.call_recieved_date.clear()
        # self.collection_date.clear()
        # self.moh_notify_date.clear()
        self.initial_issuing_info.clear()

        temp_item = Item(input)

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

        if temp_item.is_new:
            self.show_msg(SERIAL_NEVER_ISSUED)
            return

        if temp_item.is_returned:
            self.already_returned_info.set(temp_item.prev_name)
            self.already_returned_info.show()
            return

        self.form_frame.grid(row=1, column=0, pady=25)
        self.info_submit_btn.grid(row=9, column=0, pady=10)

        self.name_info.set(
            temp_item.prev_name if type(temp_item.prev_name) is str else NOT_FOUND
        )
        self.model_name_info.set(
            temp_item.model_name if type(temp_item.model_name) is str else NOT_FOUND
        )
        self.initial_issuing_info.set(
            temp_item.issuing_date if type(temp_item.issuing_date) is str else NOT_FOUND
        )

        self.item = temp_item


    def submit_info(self, info: dict[str, str | date]):
        if type(self.item) is Item and not self.item.get_serial_file_permission():
            self.show_msg(SERIAL_FILE_IN_USE)
            return
            
        res = update_record(info)

        if isinstance(res, FileNotFoundError):
            self.show_msg(SERIAL_404)
            return
        elif isinstance(res, KeyError):
            self.show_msg(MONTHLY_SHEET_404)
            return
        elif isinstance(res, PermissionError):
            self.show_msg(RECORD_FILE_IN_USE)
            return
        else:
            self.info_submit_btn.grid_forget()
        
        self.panel_set_returned()

    def panel_set_returned(self):
        if type(self.item) is Item:
            try:
                self.only_set_returned_btn.grid_forget()
                self.item.set_returned()
                self.show_msg(FILE_UPDATE_SUCCESS, is_error=False)
            except PermissionError:
                self.only_set_returned_btn.grid(row=9, column=1, pady=10)
                self.show_msg(SERIAL_FILE_IN_USE)                
        else: 
            print("item type error")

        
