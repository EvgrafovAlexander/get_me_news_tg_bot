import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
# httpx includes the complete Telegram Bot API URL (including the bot token)
# in INFO-level request logs. Keep those URLs out of application logs.
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
