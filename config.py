import sys
from pathlib import Path
from customtkinter import StringVar

# --FONTS--
GENERAL_FONT = ("arial", 17)
DATE_FONT = ("arial", 13)
BUTTON_FONT = ("arial bold", 17)
INFO_FONT = ("arial bold", 17)

# --COLORS--
FORM_FRAME_COLOR = "#2d2d2d"
BUTTON_COLOR = "#4c4c4c"

# --MESSAGES--
NOT_FOUND = "לא נמצא"
RECORD_FILE_404 = "קובץ דוחות לא נמצא"
MONTHLY_SHEET_404 = "דוח חודשי לא נמצא"
ALREADY_RETURNED_EXCEPTION = ":המוצר כבר הוחזר מלקוח קודם"

SERIAL_404 = "מספר סריאלי לא נמצא"
SERIAL_ROW_PROBLEM = "נראה כי יש בעיה עם השורה המתבקשת. אנא בדקו אותה בקובץ הסריאלי"
SERIAL_NEVER_ISSUED = "המוצר המבוקש טרם הונפק ולכן לא ייתכן כי הוחזר"
NOT_RETURNED_EXCEPTION = ":המוצר טרם הוחזר מלקוח קודם"

SERIAL_FILE_IN_USE = "קובץ הסיראלי המתבקש נמצא בשימוש, אנא דאג לסגירתו"
RECORD_FILE_IN_USE = "קובץ דוח החזרות נמצא בשימוש, אנא דאג לסגירתו"
FILE_UPDATE_SUCCESS = "הקובץ עודכן בהצלחה"
FILE_UPDATED_UNEXPECTEDLY = 'השורה עודכנה ע"י משתמש אחר. אנא הקש "חיפוש" שנית'

#--PATHS--

if getattr(sys, 'frozen', False): # as bundled executable
    app_path = Path(sys._MEIPASS) #type: ignore
    iqlc_logo_path = app_path / 'logo' / 'iqlc_nl_bright.png'
else: # as script
    app_path = Path(__file__).resolve().parent
    iqlc_logo_path = app_path / 'assets' / 'iqlc_nl_bright.png'


SERIAL_PATH = "\\\\iqlcDC\\documents$\\משרד\\סריאלי\\serial "
RECORD_PATH = "\\\\iqlcDC\\documents$\\משרד\\החזרות\\דוח החזרות.xlsx"
# SERIAL_PATH = "serial "
# RECORD_PATH = "דוח החזרות.xlsx"

SERIAL_BEGINNINGS = ["2400-03-", "2400-24-", "N220", "N160", "N50", "N60"]
MOH_DEPARTMENTS=[
    "חיפה",
    "עכו",
    "נצרת",
    "צפת",
    "עפולה",
    "טבריה",
    "חדרה",
    "ירושלים",
    "רמלה",
    "באר שבע",
    "פתח תקווה",
    "רחובות",
    "אשקלון",
    "תל אביב"
]