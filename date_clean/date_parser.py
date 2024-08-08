import re
from datetime import datetime, timedelta
from dateutil import parser
from zoneinfo import ZoneInfo

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

    # Eliminar espacios extra
    date_str = ' '.join(date_str.split())

    return date_str


def parse_relative_time(date_str, timezone="UTC"):
    now = datetime.now(ZoneInfo(timezone))

    for pattern, time_unit in RELATIVE_TIME_PATTERNS:
        match = pattern.search(date_str)
        if match:
            value = int(match.group(1))
            delta = timedelta(**{time_unit: value})
            new_time = now - delta
            return new_time.astimezone(ZoneInfo(timezone)).replace(microsecond=0).isoformat()

    if re.match(r"^\d+\s+horas?$", date_str):
        hours = int(date_str.split()[0])
        today = datetime.now(ZoneInfo(timezone)).replace(
            second=0, microsecond=0)
        new_time = today - timedelta(hours=hours)
        return new_time.astimezone(ZoneInfo(timezone)).replace(microsecond=0).isoformat()

    if re.match(r"^\d+\s+días?$", date_str):
        days = int(date_str.split()[0])
        today = datetime.now(ZoneInfo(timezone)).replace(
            second=0, microsecond=0)
        new_time = today - timedelta(days=days)
        return new_time.astimezone(ZoneInfo(timezone)).replace(microsecond=0).isoformat()

    return None


def homogenize_date(date_str, include_time=False, timezone="UTC"):
    date_str = preprocess_date_string(date_str)

    relative_date = parse_relative_time(date_str, timezone)
    if relative_date:
        return relative_date

    try:
        # Intentamos analizar la fecha como ISO 8601 primero
        try:
            date_obj = datetime.fromisoformat(date_str)
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=ZoneInfo(timezone))
            date_obj = date_obj.astimezone(ZoneInfo(timezone))
        except ValueError:
            # Si no es ISO 8601, usamos dateutil.parser.parse
            date_obj = parser.parse(
                date_str, dayfirst=True, yearfirst=False, fuzzy=True)

            # Asegura que la fecha tenga zona horaria y hora
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=ZoneInfo(timezone))

            # Si no se proporciona la hora, asumir la hora actual
            if date_obj.hour == 0 and date_obj.minute == 0 and date_obj.second == 0:
                now = datetime.now(ZoneInfo(timezone))
                date_obj = date_obj.replace(
                    hour=now.hour, minute=now.minute, second=now.second)

        # Formatear la fecha
        if include_time:
            return date_obj.astimezone(ZoneInfo(timezone)).replace(microsecond=0, second=0).isoformat()
        else:
            return date_obj.astimezone(ZoneInfo(timezone)).date().isoformat()

    except (ValueError, OverflowError):
        # Intenta manejar formatos adicionales
        date_str = date_str.strip()
        for fmt in ["%d.%m.%Y", "%Y.%m.%d", "%d/%m/%y", "%d-%b-%Y", "%d-%B-%Y", "%d/%B/%Y", "%d/%B/%y", "%A, %d %B %Y", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%d %B %Y", "%B %d, %Y", "%A, %d de %B de %Y"]:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                if date_obj.tzinfo is None:
                    date_obj = date_obj.replace(tzinfo=ZoneInfo(timezone))
                date_obj = date_obj.astimezone(ZoneInfo(timezone))

                if include_time:
                    return date_obj.astimezone(ZoneInfo(timezone)).replace(microsecond=0, second=0).isoformat()
                else:
                    return date_obj.astimezone(ZoneInfo(timezone)).date().isoformat()
            except ValueError:
                pass
        else:
            # Manejar palabras clave
            if date_str.lower() == "ayer":
                date_obj = datetime.now(ZoneInfo(timezone)) - timedelta(days=1)
            elif date_str.lower() == "hoy":
                date_obj = datetime.now(ZoneInfo(timezone))
            elif date_str.startswith("hoy a las"):
                time_str = date_str.split("hoy a las ")[1]
                try:
                    time_obj = datetime.strptime(time_str, "%H:%M")
                    date_obj = datetime.now(ZoneInfo(timezone)).replace(
                        hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                except ValueError:
                    return None
            elif date_str.lower() == "hace un momento":
                # Define un umbral para "hace un momento" (por ejemplo, 5 minutos)
                threshold = 5
                date_obj = datetime.now(
                    ZoneInfo(timezone)) - timedelta(minutes=threshold)
            else:
                return None

            if include_time:
                return date_obj.astimezone(ZoneInfo(timezone)).replace(microsecond=0, second=0).isoformat()
            else:
                return date_obj.astimezone(ZoneInfo(timezone)).date().isoformat()
