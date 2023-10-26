from customtkinter import *
from serial_module import Item

class Controller:
    def __init__(self, msgLabel: CTkLabel):
        self.msgLabel = msgLabel
        self.item = None


    def submit_serial(self,
                    input,
                    formFrame: CTkFrame,
                    nameInput: CTkEntry,
                    idInput: CTkEntry,
                    newModelInput: CTkEntry,
                    newModelFrame: CTkFrame,
                    existingModelFrame: CTkFrame,
                    existingModelName: CTkLabel,
                    prevName: CTkLabel,
                    prevNameLabel: CTkLabel,
                    deviceBirthdayDate: CTkLabel,
                    infoSubmitBtn: CTkButton,
                    deviceReturnFrame: CTkFrame,
                    deviceReturnName: CTkLabel):

        self.item = None

        self.msgLabel.grid_forget()
        existingModelFrame.grid_forget()
        newModelFrame.grid_forget()
        prevName.grid_forget()
        prevNameLabel.grid_forget()
        formFrame.grid_forget()
        infoSubmitBtn.grid_forget()
        deviceReturnFrame.grid_forget()

        clear_entry(nameInput)
        clear_entry(idInput)
        clear_entry(newModelInput)

        tempItem = Item(input)

        if isinstance(tempItem.wb, FileNotFoundError) \
        or isinstance(tempItem.sheet, KeyError) \
        or tempItem.row == -1:

            self.show_msg("מספר סריאלי לא נמצא", error=True)
            return

        if tempItem.returned or tempItem.new:
            formFrame.grid(row=2, column=1, pady=5)
            infoSubmitBtn.grid(row=4, column=1, pady=5)

        if tempItem.new:
            newModelFrame.grid(row=3, column=1, pady=5)
        else:
            existingModelFrame.grid(row=3, column=1, pady=5) 
            existingModelName.configure(text=tempItem.modelName)
            deviceBirthdayDate.configure(text = tempItem.deviceBirthday)

            if tempItem.returned:
                prevNameLabel.grid(row=0, column=1, pady=5, padx=(0, 20))
                prevName.grid(row=0, column=0, padx=10, pady=5)
                prevName.configure(text=tempItem.prevName)
            else:
                deviceReturnFrame.grid(row=4, column=1, pady=5)
                deviceReturnName.configure(text = tempItem.prevName)
            
            self.item = tempItem


    def submit_info(self, name, id, date, modelEntry: CTkEntry):
        model = modelEntry.get()
        date = date.strftime("%d/%m/%y")
        try:
            success = self.item.updateInfo(name, id, date, model)
            if not success:
                self.show_msg('השורה עודכנה ע"י משתמש אחר. אנא הקש "חיפוש" שנית', error=True)
                return
            else:
                self.show_msg("הקובץ עודכן בהצלחה", error=False)
        except PermissionError:
            self.show_msg("הקובץ המתבקש נמצא בשימוש, אנא דאג לסגירתו", error=True)


    def submit_returned(self):
        try:
            success = self.item.setReturned()
            if not success:
                self.show_msg('השורה עודכנה ע"י משתמש אחר. אנא הקש "חיפוש" שנית', error=True)
            else:
                self.show_msg("הקובץ עודכן בהצלחה", error=False)
        except PermissionError:
            self.show_msg("הקובץ המתבקש נמצא בשימוש, אנא דאג לסגירתו", error=True)

    def show_msg(self, description, error):
        self.msgLabel.configure(text=description)
        if error:
            self.msgLabel.configure(bg_color="red")
        else:
            self.msgLabel.configure(bg_color="green")
        self.msgLabel.grid(row=5, column=1)
            

def clear_entry(widget: CTkEntry):
    widget.delete(0, 'end')