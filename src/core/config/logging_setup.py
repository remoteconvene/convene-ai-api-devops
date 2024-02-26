import atexit
import sys
import threading
from datetime import datetime

import structlog
from structlog._frames import _find_first_app_frame_and_name

from src.core.config.settings import settings
from src.core.db.mongo_client_manager import mongo_client_manager


def initialize_logging():
    if mongo_client_manager.is_connected() is not True:
        print("MongoDB connection not found to initiate logging.")
        sys.exit()

    # Configure structlog to use MongoDB as a backend
    structlog.configure(
        processors=[
            mongo_processor,  # This processor logs to MongoDB
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def frame_summary_to_dict(frame_summary):
    return {
        "filename": frame_summary.filename,
        "lineno": frame_summary.lineno,
        "name": frame_summary.name,
        "line": frame_summary.line,
    }


def mongo_processor(logger, log_method, event_dict):
    # Log entry timestamp
    event_dict["timestamp"] = datetime.utcnow().isoformat()

    # Logger caller related information
    f, name = _find_first_app_frame_and_name(["logging", __name__])
    event_dict["file"] = f.f_code.co_filename
    event_dict["line"] = f.f_lineno
    event_dict["function"] = f.f_code.co_name

    # Thread related information
    current_thread = threading.current_thread()
    event_dict["thread_name"] = current_thread.name
    event_dict["thread_id"] = current_thread.ident

    # Log level
    if log_method:
        event_dict["log_level"] = log_method

    # Current log event as the message
    event_dict["msg"] = event_dict.pop("event")

    if mongo_client_manager.is_connected() is True:
        db = mongo_client_manager.mongo_client[settings.MONGODB_DATABASE]
        collection = db[settings.MONGODB_COLLECTION]
        collection.insert_one(event_dict)

    return event_dict


# MongoDB client should be closed when application exits
atexit.register(mongo_client_manager.close_client)
