from datetime import datetime, timedelta
from dateutil import parser
import re
import pytz


def uFormatDate(date_str, timezone):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M").strftime("%d/%m/%Y")
    except ValueError:
        hours_ago = int(date_str.split(" ")[1])
        now = datetime.now(pytz.timezone(timezone))
        new_date = now - timedelta(hours=hours_ago)
        return new_date.strftime("%d/%m/%Y")


def fFormatDateRelative(relative_str, include_time=False, timezone="Etc/GMT-4"):
    now = datetime.now(pytz.timezone(timezone))
    patterns = [
        (re.compile(r"hace (\d+) horas?"), "hours"),
        (re.compile(r"hace (\d+) minutos?"), "minutes"),
        (re.compile(r"hace (\d+) día[s]?"), "days"),
    ]
    delta = None
    relative_str = relative_str.lower()
    for pattern, unit in patterns:
        match = pattern.search(relative_str)
        if match:
            value = int(match.group(1))
            if unit == "hours":
                delta = timedelta(hours=value)
            elif unit == "minutes":
                delta = timedelta(minutes=value)
            elif unit == "days":
                delta = timedelta(days=value)
            break
    if delta is None:
        return None
    absolute_time = now - delta
    if include_time:
        return absolute_time.strftime("%d/%m/%Y %H:%M")
    else:
        return absolute_time.strftime("%d/%m/%Y")


def uFormatDateTimeDash(date_string, timezone="Etc/GMT-4"):
    try:
        date_parts = date_string.split(" - ")
        date_str = date_parts[0]
        time_str = date_parts[1]
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        time_obj = datetime.strptime(time_str, "%H:%M")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        formatted_time = time_obj.strftime("%H:%M")
        return f"{formatted_date} {formatted_time}"
    except ValueError:
        return None


def uFormatDateDash(date_string, timezone="Etc/GMT-4"):
    try:
        date_parts = date_string.split(" - ")
        date_str = date_parts[0]
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        return f"{formatted_date}"
    except ValueError:
        return None


def uFormatDateFromURL(url, timezone="Etc/GMT-4"):
    try:
        patron = r"-(\d+)$"
        resultado = re.search(patron, url)
        fecha = resultado.group(1)
        if len(fecha) % 2 == 0:
            fecha = fecha[0:8]
            year = fecha[:4]
            month = fecha[4:6]
            day = fecha[6:8]
        else:
            fecha = fecha[0:7]
            year = fecha[:4]
            month = fecha[4]
            day = fecha[5:7]
            month = "0" + month
        fecha_format = datetime.strptime(f"{year}{month}{day}", "%Y%m%d")
        return fecha_format.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Error al procesar la URL: {url}")
        print(f"Mensaje de error: {str(e)}")
        return None


def uFormatSpanishDate(date_str, timezone="Etc/GMT-4"):
    date_str = date_str.split(",", 1)[-1].strip()
    spanish_months = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
        "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
        "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
    }
    for spanish_month, month_number in spanish_months.items():
        date_str = date_str.lower().replace(spanish_month, month_number)
    date_str = re.sub(r"( de )(?=[\d]{4}$)", " del ", date_str)
    formats = [
        "%d de %m del %Y", "%m %d, %Y - %H:%M", "%d de %m de %Y"
    ]
    for format_str in formats:
        try:
            date_obj = datetime.strptime(date_str, format_str)
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            continue
    raise ValueError(
        f"La fecha no coincide con ninguno de los formatos conocidos Formato {format_str} no coincide con {date_str}")


def uFormatAbbrSpanishDate(date_str, timezone="Etc/GMT-4"):
    abbr_spanish_months = {
        "Ene": "01", "Feb": "02", "Mar": "03", "Abr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Ago": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dic": "12"
    }
    for abbr_spanish_month, month_number in abbr_spanish_months.items():
        date_str = date_str.replace(abbr_spanish_month, month_number)
    try:
        date_obj = datetime.strptime(date_str, "%d %m %Y, %H:%M")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        pass
    try:
        date_obj = datetime.strptime(date_str, "%d %m %Y")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        pass
    return None


def fFormatDate(date_str, include_time=False, timezone="Etc/GMT-4"):
    spanish_months = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
        "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
        "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
        "ene": "01", "feb": "02", "mar": "03", "abr": "04",
        "may": "05", "jun": "06", "jul": "07", "ago": "08",
        "sep": "09", "oct": "10", "nov": "11", "dic": "12"
    }
    spanish_weekdays = {
        "dom": "Sun", "lun": "Mon", "mar": "Tue", "mié": "Wed",
        "jue": "Thu", "vie": "Fri", "sáb": "Sat", "domingo": "Sun",
        "lunes": "Mon", "martes": "Tue", "miércoles": "Wed", "jueves": "Thu",
        "viernes": "Fri", "sábado": "Sat"
    }
    date_str = date_str.lower()
    for month_name, month_num in spanish_months.items():
        date_str = date_str.replace(month_name, month_num)
    for spanish_day, english_day in spanish_weekdays.items():
        date_str = date_str.replace(spanish_day, english_day)
    try:
        date_obj = parser.parse(date_str)
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


def homogenize_date(date_str, include_time=False, timezone="Etc/GMT-4"):
    functions = [
        uFormatDate, fFormatDateRelative, uFormatDateTimeDash,
        uFormatDateDash, uFormatDateFromURL, uFormatSpanishDate,
        uFormatAbbrSpanishDate, fFormatDate
    ]
    for func in functions:
        formatted_date = func(date_str, include_time, timezone)
        if formatted_date:
            return formatted_date
    return None
