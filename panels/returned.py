from .panel import *
from config import *
from excel_serial import Item


class ReturnedPanel(Panel):
    def __init__(self, root: CTk):
        super().__init__(root, title="דוח החזרות")

        #מספר סריאלי
        serial_input = DropListSearchBox(
            master=self.top_frame, row=1, column=0, label_text=":מספר סריאלי",
            btn_command=lambda: self.submit_serial(serial_input.get()),
            value_list=SERIAL_BEGINNINGS
        )

        self.form_frame = CTkFrame(self.main_frame, fg_color=FORM_FRAME_COLOR)

        #שם הזכאי
        self.name_info = InfoBox(
            master=self.form_frame, row=0, column=0, label_text=":שם הזכאי"
        )

        #ת.ז
        self.id_input = TextBox(
            master=self.form_frame, row=1, column=0, label_text=":ת.ז"
        )

        #לשכה
        self.department_input = TextBox(
            master=self.form_frame, row=2, column=0, label_text=":לשכה"
        )

        #מספר בקשה
        self.request_number_input = TextBox(
            master=self.form_frame, row=3, column=0, label_text=":מספר בקשה"
        )

        #סוג המכשיר
        self.model_name_info = InfoBox(
            master=self.form_frame, row=4, column=0, label_text=":מכשיר"
        )

        #תאריך קבלת פנייה
        self.call_recieved_date = DateBox(
            master=self.form_frame, row=5, column=0, label_text=":תאריך קבלת פנייה לאיסוף"
        )

        #תאריך ביצוע
        self.collection_date = DateBox(
            master=self.form_frame, row=6, column=0, label_text=":תאריך ביצוע איסוף"
        )

        #נמסרה הודעה ללשכה
        self.moh_notify_date = DateBox(
            master=self.form_frame, row=7, column=0, label_text=":תאריך מסירת הודעה ללשכה"
        )
        
        #תאריך אספקה מקורי
        self.initial_issuing_info = InfoBox(
            master=self.form_frame, row=8, column=0, label_text=":תאריך אספקה מקורי"
        )
        
        
        
    def submit_serial(self, input):
        self.item = None

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
            self.show_msg("מספר סריאלי לא נמצא", is_error=True)
            return

        if isinstance(temp_item.prev_name, AttributeError):
            self.show_msg(
                "נראה כי יש בעיה עם השורה המתבקשת. אנא בדקו אותה בקובץ הסריאלי", is_error=True
            )
            return

        if temp_item.is_new:
            self.show_msg(
                "המוצר המבוקש טרם הונפק ולכן לא ייתכן כי הוחזר", is_error=True
            )
            return

        self.form_frame.grid(row=1, column=0, pady=25)

        self.name_info.set(
            temp_item.prev_name if type(temp_item.prev_name) is str else "לא נמצא"
        )
        self.model_name_info.set(
            temp_item.model_name if type(temp_item.model_name) is str else "לא נמצא"
        )
        self.initial_issuing_info.set(
            temp_item.issuing_date if type(temp_item.issuing_date) is str else "לא נמצא"
        )

        self.item = temp_item
