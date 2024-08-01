class Status:
    NOT_STARTED = "NOT_STARTED"
    PROCESSING = "PROCESSING"
    DOWNLOADING = "DOWNLOADING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

DOWNLOAD_MAX_RETRIES = 3
DOWNLOAD_RETRY_INTERVAL_SEC = 5
DOWNLOAD_TIMEOUT_SEC = 600
NEXT_CHECK_TIME_INTERVAL_SEC = 300
