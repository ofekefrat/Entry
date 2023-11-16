from tkcalendar import DateEntry
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkFont, CTkEntry, CTkComboBox
from config import *
from typing import Callable, List

ELEMENT_PADX = 10
ELEMENT_PADY = 5
DEFAULT_LABEL_COLUMN = 2

class LabelColumnException(Exception):
    def __init__(self) -> None:
        super().__init__("label_column must be greater than or equal to 1")

class SearchBoxColumnException(Exception):
    def __init__(self) -> None:
        super().__init__("label_column must be greater than or equal to 2 in a SearchBox")
    
class DroplistSearchBoxColumnException(Exception):
    def __init__(self) -> None:
        super().__init__("label_column must be greater than or equal to 3 in a DroplistSearchBox")

class LabeledBox:
    """Parent class for labeled boxes"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 label_text: str,
                 row: int,
                 label_column: int = DEFAULT_LABEL_COLUMN
                 ):
        self.background = master.cget("fg_color")
        self.row = row
        if label_column < 1:
            raise LabelColumnException
        self.label_column = label_column
        self.element_column = label_column-1
        # self.frame = CTkFrame(master, fg_color=self.background)

        self.label = CTkLabel(
            master=master,
            font=GENERAL_FONT,
            text=label_text,
            bg_color=self.background,
        )
        self.label.grid(column=self.label_column, row=self.row, pady=ELEMENT_PADY, padx=ELEMENT_PADX)
        self.stringvar = StringVar()
    
    def show(self):
        self.label.grid(column=self.label_column, row=self.row, pady=ELEMENT_PADY, padx=ELEMENT_PADX)

    def hide(self):
        self.label.grid_forget()

    def clear(self):
        self.stringvar.set("")
        
    def set(self, text: str):
        self.stringvar.set(text)

    def get(self) -> str:
        return self.stringvar.get()

class InfoBox(LabeledBox):
    """Info box with a label next to it."""
    def __init__(self,
                 master: CTk | CTkFrame,
                 label_text: str,
                 row: int,
                 label_column: int = DEFAULT_LABEL_COLUMN,
                 ):
        super().__init__(master, label_text, row, label_column)
        
        self.info = CTkLabel(
            master=master,
            font=INFO_FONT,
            fg_color=self.background,
            textvariable=self.stringvar
        )
        self.info.grid(column=self.element_column, row=self.row, padx=ELEMENT_PADX)

    def show(self):
        super().show()
        self.info.grid(column=self.element_column, row=self.row, pady=ELEMENT_PADY, padx=ELEMENT_PADX)

    def hide(self):
        super().hide()
        self.info.grid_forget()

    # def get(self) -> str:
    #     return self.stringvar.get()
    #     # return self.info.cget("text")
        
    # def set(self, text: str):
    #     self.stringvar.set(text)
    #     # self.info.configure(text=text)
    
    # def clear(self):
    #     self.info.configure(text="")


class DateBox(LabeledBox):
    """Date selection/input with a label next to it"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 label_text: str,
                 row: int,
                 label_column : int = DEFAULT_LABEL_COLUMN,
                 ):
        super().__init__(master, label_text, row, label_column)
        
        self.date_input = DateEntry(
            master=master,
            date_pattern = "dd/mm/yy",
            font=DATE_FONT,
            justify="center"
        )
        self.date_input.grid(column=self.element_column, row=self.row, padx=ELEMENT_PADX)

    def get(self):
        return self.date_input.get_date()

    def show(self):
        super().show()
        self.date_input.grid(column=self.element_column, row=self.row, padx=ELEMENT_PADX)
    
    def clear(self):
        print("nope")

    def hide(self):
        super().hide()
        self.date_input.grid_forget()


class TextBox(LabeledBox):
    """Text box with a label next to it"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 label_text: str,
                 row: int,
                 label_column: int = DEFAULT_LABEL_COLUMN,
                 ):
        super().__init__(master, label_text, row, label_column)

        self.input = CTkEntry(
            master=master,
            textvariable=self.stringvar,
            bg_color=self.background,
            font=GENERAL_FONT,
            justify='right'
        )
        self.input.grid(column=self.element_column, row=self.row, padx=ELEMENT_PADX)

    def show(self):
        super().show()
        self.input.grid(column=self.element_column, row=self.row, padx=ELEMENT_PADX)

    def hide(self):
        super().hide()
        self.input.grid_forget()

    # def get(self) -> str:
    #     return self.input.get()

    # def clear(self):
    #     self.input.delete(0, "end")

class DroplistTextBox(LabeledBox):
    """Labeled text box with a droplist"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 label_text: str,
                 row: int,
                 values: List[str],
                 label_column: int = DEFAULT_LABEL_COLUMN,
                 ):
        super().__init__(master=master, label_text=label_text, row=row, label_column=label_column)
        
        self.box = CTkComboBox(
            master=master,
            variable=self.stringvar,
            values=values,
            bg_color=self.background,
            font=GENERAL_FONT,
            dropdown_font=GENERAL_FONT,
            justify='right'
        )
        self.box.grid(column=self.element_column, row=self.row, padx=ELEMENT_PADX)

    def show(self):
        super().show()
        self.box.grid(column=self.element_column, row=self.row, padx=ELEMENT_PADX)

    def hide(self):
        super().hide()
        self.box.grid_forget()


class SearchBox(TextBox):
    """Search box"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 label_text: str,
                 row: int,
                 btn_command: Callable,
                 label_column: int = DEFAULT_LABEL_COLUMN+1,
                 ):
        if label_column < 2: raise SearchBoxColumnException 
        super().__init__(master=master, label_text=label_text, row=row, label_column=label_column)

        self.btn_column = label_column-3 if type(self) is DropListSearchBox else label_column-2
        
        self.btn = CTkButton( fg_color=BUTTON_COLOR,
            master=master,
            text="חפש",
            bg_color=self.background,
            font=BUTTON_FONT,
            command=btn_command,
            width=10
        )
        self.btn.grid(column=self.btn_column, row=self.row, padx=ELEMENT_PADX)

    def show(self):
        super().show()
        self.btn.grid(column=self.btn_column, row=self.row, padx=ELEMENT_PADX)

    def hide(self):
        super().hide()
        self.btn.grid_forget()

class DropListSearchBox(SearchBox):
    """Search box with droplist"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 label_text: str,
                 row: int,
                 btn_command: Callable,
                 value_list: List[str],
                 label_column : int = DEFAULT_LABEL_COLUMN+2,
                 ):
        if label_column < 3: raise DroplistSearchBoxColumnException
        super().__init__(master=master, label_text=label_text, row=row, label_column=label_column, btn_command=btn_command)

        self.droplist_column = label_column-2
        self.input.configure(justify="left")
        
        self.droplist = CTkOptionMenu(
            master=master,
            bg_color=self.background,
            fg_color=self.input.cget("fg_color"),
            button_color=self.input.cget("fg_color"),
            button_hover_color="gray",
            font=GENERAL_FONT,
            anchor="e",
            width=20,
            values=value_list
        )
        self.droplist.grid(column=self.droplist_column, row=self.row)

    def get(self) -> str:
        return self.droplist.get() + self.stringvar.get()

    def show(self):
        super().show()
        self.droplist.grid(column=self.droplist_column, row=self.row, padx=ELEMENT_PADX)

    def hide(self):
        super().hide()
        self.droplist.grid_forget()

class Panel:
    """Parent class for panels"""
    def __init__(self,
                 root: CTk | CTkFrame,
                 title: str
                 ):
        self.serial_input: DropListSearchBox
        self.root = root
        self.background = root.cget("fg_color")
        self.main_frame = CTkFrame(root, bg_color=self.background, fg_color=self.background)
        self.top_frame = CTkFrame(self.main_frame, bg_color=self.background, fg_color=self.background)
        self.top_frame.grid(row=0, column=0)

        self.msg_label = CTkLabel(
            self.main_frame, text_color="white", font=GENERAL_FONT, corner_radius=5
        )

        self.title = CTkLabel(
            master=self.top_frame, text=title,
            font=CTkFont("arial", 23, underline=True),
            bg_color=self.background
        )
        self.title.grid(row=0, column=3, pady=30)

        self.main_frame.bind()

    
    def start(self):
        self.main_frame.grid(column=0, row=1)
        self.serial_input.input.focus_set()

    def stop(self):
        self.main_frame.grid_forget()

    def show_msg(self, msg_text, is_error=True):
        self.msg_label.configure(text=msg_text)
        if is_error:
            self.msg_label.configure(bg_color="red")
        else:
            self.msg_label.configure(bg_color="green")
        self.msg_label.grid(row=10, column=0)

    def submit_serial(self):
        print("panel")
        pass

    def submit_info(self):
        pass
