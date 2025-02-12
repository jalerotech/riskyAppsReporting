from datetime import datetime, timezone
import logging
logger = logging.getLogger('Refresher timer check')

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


def timeToRefresh(token_expiry_time):
    """
    Checks if the time difference between the token expiry time and current time is less than or equal to token expiry time (3600 seconds).
    :param token_expiry_time: initial time of token request.
    :return: bool
    """

    logger.info("Checking if token_request_time and current time is less than or equal to token expiry time.")

    current_time_utc = datetime.now(timezone.utc)

    # Convert the datetime objects to Unix timestamps
    token_request_time_unix = int(token_expiry_time)
    current_time_unix = int(current_time_utc.timestamp())

    # Calculate the absolute difference in seconds
    time_difference_seconds = abs(current_time_unix - token_request_time_unix)
    logger.info(f"time_difference_seconds -> {time_difference_seconds}")
    if time_difference_seconds <= 100:
        logger.info(f"Bearer token expiring in less than {time_difference_seconds}. Triggering refresh.")
        return True
    else:
        logger.info(f"Current bearer token still valid for {time_difference_seconds}")
        return False
