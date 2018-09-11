
from numpy import random
from scipy.fftpack import fft

from celery import shared_task
from proj import celery_app
from celery.utils.log import get_task_logger

from celery_progress.backend import ProgressRecorder

logger = get_task_logger(__name__)


# The @shared_task decorator lets you create tasks without having any concrete
# app instance. Ignore results doesn't write results into database
@shared_task(ignore_result=True)
def hello():
    logger.info("Logging hello")
    print("Hello there!")


# define task in a celery queue
@celery_app.task(bind=True)
def add(self, x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y


# A task being bound means the first argument to the task will always be
# the task instance (self), just like Python bound methods:
@celery_app.task(bind=True)
def mul(self, x, y):
    return x * y


@celery_app.task(bind=True)
def xsum(self, numbers):
    return sum(numbers)


# https://www.codementor.io/uditagarwal/asynchronous-tasks-using-celery-with-django-du1087f5k
@shared_task(bind=True)
def fft_random(self, n):
    progress_recorder = ProgressRecorder(self)

    for i in range(n):
        x = random.normal(0, 0.1, 2000)
        y = fft(x)

        progress_recorder.set_progress(i + 1, n)

    return "done"
