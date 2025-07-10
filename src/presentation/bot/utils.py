from datetime import date


def get_ru_format_date(dt: date) -> str:
    return dt.strftime("%d.%m.%Y")
