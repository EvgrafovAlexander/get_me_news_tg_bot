import asyncio
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.app import create_bot_app
from config.settings import settings
from logger import logger
from services.db import init_db
from tasks import check_all_sources, run_bot, weekly_cleanup_job


async def run_scheduler():
    """Запускает APScheduler с выполнением периодической задачи check_all_sources"""
    refresh_minutes = settings.rss_refresh_minutes

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_all_sources, "interval", minutes=refresh_minutes)
    scheduler.add_job(weekly_cleanup_job, "cron",   day_of_week="mon", hour=4, minute=0)
    scheduler.start()

    logger.info(
        f"Scheduler started. Interval: {refresh_minutes} minutes, "
        f"cleanup every 1 week."
    )


async def main():
    # Создаем и запускаем экземпляр бота
    bot_app = create_bot_app()
    asyncio.create_task(run_bot(bot_app))

    # Запускаем APScheduler с задачами check_all_sources, weekly_cleanup_job
    asyncio.create_task(run_scheduler())

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    init_db()
    if settings.manual_run:
        logger.info("MANUAL_RUN enabled — running check_all_sources once.")
        asyncio.run(check_all_sources())
    else:
        asyncio.run(main())
