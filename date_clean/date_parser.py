import re
from datetime import datetime, timedelta
from dateutil import parser
from zoneinfo import ZoneInfo  # Importamos ZoneInfo

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


# Cambiamos el timezone por defecto a UTC
def parse_relative_time(date_str, timezone="UTC"):
    now = datetime.now(ZoneInfo(timezone))  # Usamos ZoneInfo

    for pattern, time_unit in RELATIVE_TIME_PATTERNS:
        match = pattern.search(date_str)
        if match:
            value = int(match.group(1))
            delta = timedelta(**{time_unit: value})
            new_time = now - delta
            # Usamos ZoneInfo
            return new_time.astimezone(ZoneInfo(timezone)).replace(microsecond=0).isoformat()

    # Si no coincide con ningún patrón relativo, asumimos que es solo la hora o el día
    if re.match(r"^\d+\s+horas?$", date_str):
        hours = int(date_str.split()[0])
        today = datetime.now(ZoneInfo(timezone)).replace(
            second=0, microsecond=0)  # Usamos ZoneInfo
        new_time = today - timedelta(hours=hours)
        # Usamos ZoneInfo
        return new_time.astimezone(ZoneInfo(timezone)).replace(microsecond=0).isoformat()

    if re.match(r"^\d+\s+días?$", date_str):
        days = int(date_str.split()[0])
        today = datetime.now(ZoneInfo(timezone)).replace(
            second=0, microsecond=0)  # Usamos ZoneInfo
        new_time = today - timedelta(days=days)
        # Usamos ZoneInfo
        return new_time.astimezone(ZoneInfo(timezone)).replace(microsecond=0).isoformat()

    return None


# Cambiamos el timezone por defecto a UTC
def homogenize_date(date_str, include_time=False, timezone="UTC"):
    date_str = preprocess_date_string(date_str)

    relative_date = parse_relative_time(date_str, timezone)
    if relative_date:
        return relative_date

    try:
        # Intentamos analizar la fecha como ISO 8601 primero
        try:
            date_obj = datetime.fromisoformat(date_str)
            # Si la fecha no tiene zona horaria, le asignamos la zona horaria del usuario
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=ZoneInfo(timezone))
            # Convertimos la fecha a la zona horaria del usuario
            date_obj = date_obj.astimezone(ZoneInfo(timezone))
        except ValueError:
            # Si no es ISO 8601, usamos dateutil.parser.parse
            date_obj = parser.parse(
                date_str, dayfirst=True, yearfirst=False, fuzzy=True)

            # Asegura que la fecha tenga zona horaria y hora
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(
                    tzinfo=ZoneInfo(timezone))  # Usamos ZoneInfo

            # Si no se proporciona la hora, asumir la hora actual
            if date_obj.hour == 0 and date_obj.minute == 0 and date_obj.second == 0:
                now = datetime.now(ZoneInfo(timezone))  # Usamos ZoneInfo
                date_obj = date_obj.replace(
                    hour=now.hour, minute=now.minute, second=now.second)

        if include_time:
            # Eliminamos los segundos para evitar errores de precisión
            # Usamos ZoneInfo
            return date_obj.astimezone(ZoneInfo(timezone)).replace(microsecond=0, second=0).isoformat()
        else:
            # Usamos ZoneInfo
            return date_obj.astimezone(ZoneInfo(timezone)).date().isoformat()

    except (ValueError, OverflowError):
        return None
