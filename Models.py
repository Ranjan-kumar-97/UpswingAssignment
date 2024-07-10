from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Union
from Helper import parse_datetime

class TimeRange(BaseModel):
    """
    A Pydantic model that represents a time range with start and end times.
    The times can be provided as datetime objects, strings, or Unix timestamps,
    and are converted to Unix timestamps during validation.

    Attributes:
        start_time (Union[datetime, str, int]): The start time of the range.
        end_time (Union[datetime, str, int]): The end time of the range.
    """
    
    start_time: Union[datetime, str, int]
    end_time: Union[datetime, str, int]

    @model_validator(mode='before')
    def convert_to_datetime(cls, values):
        """
        A model validator that converts start and end times to Unix timestamps
        before validation. It also ensures that the end time is greater than the start time.

        Args:
            values (dict): A dictionary of the field values to be validated.

        Returns:
            dict: The validated and possibly modified field values.

        Raises:
            ValueError: If the end time is not greater than the start time.
        """
        start_time = values.get('start_time')
        end_time = values.get('end_time')
        
        if start_time is not None:
            values['start_time'] = parse_datetime(start_time).timestamp()
        
        if end_time is not None:
            values['end_time'] = parse_datetime(end_time).timestamp()
        
        if values['end_time'] <= values['start_time']:
            raise ValueError('end_time must be greater than start_time')
        
        return values
