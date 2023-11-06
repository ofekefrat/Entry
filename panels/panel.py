from customtkinter import *
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
        self.frame = CTkFrame(master, fg_color=self.background)

        self.label = CTkLabel(
            master = self.frame, 
            font = general_font,
            text = label_text,
            bg_color = self.background
        )
        self.label.grid(column=3, row=0)
        self.show()
    
    def show(self):
        self.frame.grid(row=self.row, column=self.column, pady=5, sticky='e')

    def clear(self):
        pass
    
    def get(self) -> str:
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
            master=self.frame,
            bg_color=self.background,
            font=info_font
        )
        self.info.grid(column=2, row=0, padx=10)

    def get(self) -> str:
        return self.info.cget("text")
    
    def clear(self):
        self.info.configure(text="")


class TextBox(LabeledBox):
    """Text box with a label next to it."""
    def __init__(self,
                 master: CTk | CTkFrame,
                 row,
                 column,
                 label_text: str
                 ):
        super().__init__(master, row, column, label_text)

        self.input = CTkEntry(
            master=self.frame,
            bg_color=self.background,
            font=general_font,
            justify='right'
        )
        self.input.grid(column=2, row=0, padx=10)

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
            master=self.frame,
            text="חפש",
            bg_color=self.background,
            font=general_font,
            command=btn_command,
            width=10
        )
        self.btn.grid(column=0, row=0, padx=10)


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
        
        self.droplist = CTkOptionMenu(
            master=self.frame,
            bg_color=self.background,
            fg_color="white",
            button_color="white",
            button_hover_color="gray",
            font=general_font,
            text_color="black",
            anchor="e",
            width=20,
            values=value_list
        )
        self.btn.grid(column=1, row=0)

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

        self.msg_label = CTkLabel(
            self.main_frame, text_color="white", font=general_font, corner_radius=5
        )

        self.title = CTkLabel(
            self.main_frame,
            text=title,
            font=CTkFont("arial", 23, underline=True),
            bg_color=self.background
        )
        self.title.grid(row=0, column=0, pady=30)

    
    def start(self):
        self.main_frame.pack()

    def stop(self):
        self.main_frame.pack_forget()

    # def clear_entry(widget: CTkEntry | LabeledBox):
    #     widget.delete(0, "end")

    def show_msg(self, msg_text, is_error):
        self.msg_label.configure(text=msg_text)
        if is_error:
            self.msg_label.configure(bg_color="red")
        else:
            self.msg_label.configure(bg_color="green")
        self.msg_label.grid(row=10, column=1)
        