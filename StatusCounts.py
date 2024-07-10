from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Models import TimeRange
from ConnectMongo import collection


async def get_status_counts(time_range: TimeRange):
    """
    Get the count of each status within a specified time range.

    This function constructs an aggregation pipeline to match documents
    within the specified time range and groups them by status to count
    the occurrences of each status.

    Args:
        time_range (TimeRange): The time range for which to get the status counts.

    Returns:
        JSONResponse: A JSON response containing the counts of each status within the specified time range.

    Raises:
        HTTPException: If a ValueError occurs during processing, a 400 status code with the error details is returned.
    """
    try:
        start_time = time_range.start_time.timestamp()
        end_time = time_range.end_time.timestamp()
        print(start_time)
        print(end_time)
        
        pipeline = [
            {
                "$match": {
                    "timestamp": {
                        "$gte": start_time,
                        "$lte": end_time
                    }
                }
            },
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1}
                }
            }
        ]

        result = list(collection.aggregate(pipeline))
        status_counts = {item["_id"]: item["count"] for item in result}
        return JSONResponse(content=status_counts)
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
