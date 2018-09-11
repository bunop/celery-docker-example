import json

from django.shortcuts import render
from django.http import HttpResponse

from celery.result import AsyncResult

from .tasks import fft_random


# Create your views here.
def task_state(request):
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def index(request):
    return render(
        request,
        'app/index.html',
        )


def progress_view(request):
    result = fft_random.delay(10000)

    return render(
        request,
        'app/display_progress.html',
        context={'task_id': result.task_id})
