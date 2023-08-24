from django.http import JsonResponse
from django.middleware.csrf import get_token


def get_csrf_token(request):
    csrftoken = get_token(request)
    # print(csrftoken)
    return JsonResponse({'csrftoken': csrftoken})