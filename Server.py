import threading
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from contextlib import asynccontextmanager
from Models import TimeRange
from Consumer import consume, rabbitmq_state
from StatusCounts import get_status_counts

Server = FastAPI()

@asynccontextmanager
async def lifespan(Server: FastAPI):
    """
    Async context manager for managing the lifecycle of the FastAPI server.

    This context manager starts a RabbitMQ consumer thread when the server starts
    and shuts it down gracefully when the server stops.

    Args:
        Server (FastAPI): The FastAPI server instance.
    """
    consumer_thread = threading.Thread(target=consume)
    consumer_thread.start()
    try:
        yield
    finally:
        print("Shutting down RabbitMQ consumer")
        if rabbitmq_state.channel:
            rabbitmq_state.channel.stop_consuming()
        if rabbitmq_state.connection:
            rabbitmq_state.connection.close()
        print("RabbitMQ consumer shut down")
        consumer_thread.join()

# Set the lifespan context manager for the server
Server.router.lifespan_context = lifespan

@Server.post("/status_counts")
async def status_counts_endpoint(time_range: TimeRange):
    """
    Endpoint to get the count of each status within a specified time range.

    Args:
        time_range (TimeRange): The time range for which to get the status counts.

    Returns:
        JSONResponse: The counts of each status within the specified time range.
    """
    return await get_status_counts(time_range)

@Server.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler for request validation errors.

    Args:
        request (Request): The incoming request.
        exc (RequestValidationError): The validation error exception.

    Returns:
        JSONResponse: A response with status code 422 and an error message.
    """
    return JSONResponse(
        status_code=422,
        content={"message": "Invalid input, please check your request data."},
    )

@Server.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """
    Custom exception handler for Pydantic validation errors.

    Args:
        request (Request): The incoming request.
        exc (ValidationError): The Pydantic validation error exception.

    Returns:
        JSONResponse: A response with status code 400 and an error message.
    """
    return JSONResponse(
        status_code=400,
        content={"message": "Invalid input, please check your request data."},
    )

@Server.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Custom exception handler for general exceptions.

    Args:
        request (Request): The incoming request.
        exc (Exception): The exception.

    Returns:
        JSONResponse: A response with status code 500 and an error message.
    """
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."},
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(Server, host="0.0.0.0", port=8000)
