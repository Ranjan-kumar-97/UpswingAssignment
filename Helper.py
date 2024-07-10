from datetime import datetime

def parse_datetime(v):
    """
    Parses a given value into a datetime object.

    This function attempts to parse the input value into a datetime object.
    It supports multiple date formats for string inputs and can handle Unix timestamps.

    Args:
        v (Union[str, int, datetime]): The value to be parsed. It can be a string, an integer (Unix timestamp), or a datetime object.

    Returns:
        datetime: The parsed datetime object.

    Raises:
        ValueError: If the input value cannot be parsed into a datetime object.
    """
    date_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    if isinstance(v, str):
        for fmt in date_formats:
            try:
                return datetime.strptime(v, fmt)
            except ValueError:
                continue
        raise ValueError("Invalid datetime format")
    elif isinstance(v, int):
        return datetime.fromtimestamp(v)
    elif isinstance(v, datetime):
        return v
    else:
        raise ValueError("Invalid type for datetime parsing")
