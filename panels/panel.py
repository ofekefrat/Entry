from tkcalendar import DateEntry
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkFont, CTkEntry
from config import *
from typing import Callable, List


class LabeledBox:
    """Parent class for labeled boxes"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 row,
                 column,
                 label_text: str
                 ):
        self.background = master.cget("fg_color")
        self.row = row
        self.column = column
        # self.frame = CTkFrame(master, fg_color=self.background)

        self.label = CTkLabel(
            master = master,
            font = GENERAL_FONT,
            text = label_text,
            bg_color = self.background,
        )
        self.label.grid(column=3, row=self.row, pady=5, padx=10)
    
    def show(self):
        self.label.grid(column=3, row=self.row, pady=5, padx=10)

    def hide(self):
        self.label.grid_forget()

    def clear(self):
        pass
    
    def get(self):
        pass


class InfoBox(LabeledBox):
    """Info box with a label next to it."""
    def __init__(self,
                 master: CTk | CTkFrame,
                 row,
                 column,
                 label_text: str
                 ):
        super().__init__(master, row, column, label_text)
        
        self.info = CTkLabel(
            master=master,
            font=INFO_FONT,
            fg_color=self.background
        )
        self.info.grid(column=2, row=self.row, padx=10)

    def show(self):
        super().show()
        self.info.grid(column=2, row=self.row, pady=5, padx=10)

    def hide(self):
        super().hide()
        self.info.grid_forget()

    def get(self) -> str:
        return self.info.cget("text")
        
    def set(self, text: str):
        self.info.configure(text=text)
    
    def clear(self):
        self.info.configure(text="")


class DateBox(LabeledBox):
    """Date selection/input with a label next to it"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 row,
                 column,
                 label_text: str
                 ):
        super().__init__(master, row, column, label_text)
        
        self.date_input = DateEntry(
            master=master,
            date_pattern = "dd/mm/yy",
            font=DATE_FONT,
            justify="center"
        )
        self.date_input.grid(column=2, row=self.row, padx=10)

    def get(self):
        return self.date_input.get_date()

    # def clear(self): do this someday maybe
    #     self.date_input.configure()


class TextBox(LabeledBox):
    """Text box with a label next to it"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 row,
                 column,
                 label_text: str
                 ):
        super().__init__(master, row, column, label_text)

        self.input = CTkEntry(
            master=master,
            bg_color=self.background,
            font=GENERAL_FONT,
            justify='right'
        )
        self.input.grid(column=2, row=self.row, padx=10)

    def show(self):
        super().show()
        self.input.grid(column=2, row=self.row, padx=10)

    def hide(self):
        super().hide()
        self.input.grid_forget()

    def get(self) -> str:
        return self.input.get()

    def clear(self):
        self.input.delete(0, "end")


class SearchBox(TextBox):
    """Search box"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 row,
                 column,
                 label_text: str,
                 btn_command: Callable
                 ):
        super().__init__(master, row, column, label_text)
        
        self.btn = CTkButton(
            master=master,
            text="חפש",
            bg_color=self.background,
            font=GENERAL_FONT,
            command=btn_command,
            width=10
        )
        self.btn.grid(column=0, row=self.row, padx=10)


class DropListSearchBox(SearchBox):
    """Search box with droplist"""
    def __init__(self,
                 master: CTk | CTkFrame,
                 row,
                 column,
                 label_text: str,
                 btn_command: Callable,
                 value_list: List[str]
                 ):
        super().__init__(master, row, column, label_text, btn_command)
        
        self.input.configure(justify="left")
        
        self.droplist = CTkOptionMenu(
            master=master,
            bg_color=self.background,
            fg_color="white",
            button_color="white",
            button_hover_color="gray",
            font=GENERAL_FONT,
            text_color="black",
            anchor="e",
            width=20,
            values=value_list
        )
        self.droplist.grid(column=1, row=self.row)

    def get(self) -> str:
        return self.droplist.get() + self.input.get()


class Panel:
    """Parent class for panels"""
    def __init__(self,
                 root: CTk,
                 title: str
                 ):
        self.root = root
        self.background = root.cget("fg_color")
        self.main_frame = CTkFrame(root, bg_color=self.background, fg_color=self.background)
        self.top_frame = CTkFrame(self.main_frame, bg_color=self.background, fg_color=self.background)
        self.top_frame.grid(row=0, column=0)

        self.msg_label = CTkLabel(
            self.main_frame, text_color="white", font=GENERAL_FONT, corner_radius=5
        )

        self.title = CTkLabel(
            self.top_frame,
            text=title,
            font=CTkFont("arial", 23, underline=True),
            bg_color=self.background
        )
        self.title.grid(row=0, column=2, pady=30)

    
    def start(self):
        self.main_frame.pack()

    def stop(self):
        self.main_frame.pack_forget()

    def show_msg(self, msg_text, is_error=True):
        self.msg_label.configure(text=msg_text)
        if is_error:
            self.msg_label.configure(bg_color="red")
        else:
            self.msg_label.configure(bg_color="green")
        self.msg_label.grid(row=10, column=0)
        