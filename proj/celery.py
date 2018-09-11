import os
from celery import Celery, Task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from django.core import management


logger = get_task_logger(__name__)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


class MyTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def debug_task(self):
        print('Request: {0!r}'.format(self.request))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

    sender.add_periodic_task(
        crontab(minute="*/30"),
        cleanup.s(),
    )

    sender.add_periodic_task(
        crontab(minute="*/5"),
        fail.s(),
    )


# task inheritance
@app.task(bind=True, base=MyTask)
def test(self, arg):
    print(arg)


# https://stackoverflow.com/a/51429597
@app.task(bind=True, base=MyTask)
def cleanup(self):
    """Cleanup expired sessions by using Django management command."""

    logger.info("Clearing session with celery")
    self.debug_task()

    management.call_command("clearsessions", verbosity=1)
    # PUT MANAGEMENT COMMAND HERE

    return "success"


@app.task(bind=True, base=MyTask)
def fail(self):
    raise Exception("Testing an exception")
