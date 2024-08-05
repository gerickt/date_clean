import re
from datetime import datetime, timedelta
from dateutil import parser
import pytz

SPANISH_MONTHS = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
    "ene": "01", "feb": "02", "mar": "03", "abr": "04",
    "may": "05", "jun": "06", "jul": "07", "ago": "08",
    "sep": "09", "oct": "10", "nov": "11", "dic": "12"
}

SPANISH_WEEKDAYS = {
    "dom": "Sun", "lun": "Mon", "mar": "Tue", "mié": "Wed",
    "jue": "Thu", "vie": "Fri", "sáb": "Sat", "domingo": "Sun",
    "lunes": "Mon", "martes": "Tue", "miércoles": "Wed", "jueves": "Thu",
    "viernes": "Fri", "sábado": "Sat"
}

RELATIVE_TIME_PATTERNS = [
    (re.compile(r"hace (\d+) horas?"), "hours"),
    (re.compile(r"hace (\d+) minutos?"), "minutes"),
    (re.compile(r"hace (\d+) días?"), "days"),
]


def preprocess_date_string(date_str):
    date_str = date_str.lower()

    for spanish_month, month_num in SPANISH_MONTHS.items():
        date_str = date_str.replace(spanish_month, month_num)

    for spanish_day, english_day in SPANISH_WEEKDAYS.items():
        date_str = date_str.replace(spanish_day, english_day)

    date_str = re.sub(r"[^\w\s/:,-]", "", date_str)
    return date_str


def parse_relative_time(date_str, timezone):
    now = datetime.now(pytz.timezone(timezone))

    for pattern, time_unit in RELATIVE_TIME_PATTERNS.items():
        match = pattern.search(date_str)
        if match:
            value = int(match.group(1))
            delta = timedelta(**{time_unit: value})
            return (now - delta).strftime("%d/%m/%Y %H:%M")

    return None


def homogenize_date(date_str, include_time=False, timezone="America/La_Paz"):
    date_str = preprocess_date_string(date_str)

    relative_date = parse_relative_time(date_str, timezone)
    if relative_date:
        return relative_date

    try:
        date_obj = parser.parse(date_str, fuzzy=True)
        user_timezone = pytz.timezone(timezone)
        if date_obj.tzinfo is None:
            date_obj = user_timezone.localize(date_obj)
        else:
            date_obj = date_obj.astimezone(user_timezone)

        if include_time:
            return date_obj.strftime("%d/%m/%Y %H:%M")
        else:
            return date_obj.strftime("%d/%m/%Y")
    except (ValueError, OverflowError):
        return None
