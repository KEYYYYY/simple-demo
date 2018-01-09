import subprocess

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

setting = {
    'DEBUG': True,
    'ROOT_URLCONF': __name__,
}

settings.configure(**setting)


def index(request):
    with open('index.html', 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def run_code(code):
    """
    执行客户端发来代码的函数
    """
    try:
        output = subprocess.check_output(
            ['python', '-c', code],
            universal_newlines=True,
            stderr=subprocess.STDOUT,
            timeout=3
        )
    except subprocess.CalledProcessError as e:
        print(e.output)
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = '运行超时' + e.output
    return output


@csrf_exempt
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse({
        'output': output,
    })


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^api/$', api, name='api'),
]

if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
