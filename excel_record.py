from _pydatetime import date
from openpyxl import load_workbook
from config import RECORD_PATH

DATE_TO_SHEET_NAME = {
    1: "ינואר",
    2: "פברואר",
    3: "מרץ",
    4: "אפריל",
    5: "מאי",
    6: "יוני",
    7: "יולי",
    8: "אוגוסט",
    9: "ספטמבר",
    10: "אוקטובר",
    11: "נובמבר",
    12: "דצמבר"
}

COLUMN_FOR_DATA = {
    "name": "A",
    "id": "B",
    "department": "C",
    "request" : "D",
    "model": "E",
    "serial": "F",
    "call_recieved": "I",
    "collection_date": "J",
    "moh_nofitied_date": "K",
    "initial_issuing_date": "L"
}

def update_record(info: dict[str, str | date]):
    file_name = RECORD_PATH

    try:    
        wb = load_workbook(file_name)
    except FileNotFoundError as e:
        return e

    try:
        sheet = wb[f"דוח החזרות {DATE_TO_SHEET_NAME[info["collection_date"].month]}"] #type: ignore
    except KeyError as e:
        return e

    row = 0
    for cell in sheet["A"]:
        if cell.value is None:
            row = cell.row
            break
        
    col_names = [
        "name",
        "id",
        "department",
        "request",
        "model",
        "serial",
        "call_recieved",
        "collection_date",
        "moh_nofitied_date",
        "initial_issuing_date"
    ]

    for cn in col_names:
        if type(info[cn]) is date:
            sheet[f"{COLUMN_FOR_DATA[cn]}{row}"] = info[cn].strftime("%d/%m/%y") # type: ignore
        else:
            sheet[f"{COLUMN_FOR_DATA[cn]}{row}"] = info[cn] # type: ignore

    try:
        wb.save(file_name)
        return True
    except PermissionError as e:
        return e
        