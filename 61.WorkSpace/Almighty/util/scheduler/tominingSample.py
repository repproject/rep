import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler

logging = logging.getLogger(__name__)

def tick():
    logger.debug('tick!!!')

sched = BackgroundScheduler()
sched.add_job(tick,interval, seconds=3)
sched.start()

