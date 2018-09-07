from celery import shared_task
from proj import celery_app
from celery.utils.log import get_task_logger
from django.core import management

logger = get_task_logger(__name__)


# The @shared_task decorator lets you create tasks without having any concrete
# app instance. Ignore results doesn't write results into database
@shared_task(ignore_result=True)
def hello():
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


# https://stackoverflow.com/a/51429597
@celery_app.task
def cleanup():
    """Cleanup expired sessions by using Django management command."""
    try:
        logger.info("Clearing session with celery")
        management.call_command("clearsessions", verbosity=1)
        # PUT MANAGEMENT COMMAND HERE
        return "success"

    except Exception as e:
        print(e)
