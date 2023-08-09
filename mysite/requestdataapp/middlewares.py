from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


def set_useragent_on_request_middleware(get_response):
    print('initial call')

    def middleware(request: HttpRequest):
        print("before get_response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print('after get_response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self.requests_count += 1
        print(f"requests count {self.requests_count}")
        response = self.get_response(request)
        self.responses_count += 1
        print(f"responses count {self.responses_count}")
        return response


class ThrottlingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Получение IP-адреса пользователя
        ip_address = request.META.get('REMOTE_ADDR')

        # Проверка, превышен ли лимит запросов для данного IP-адреса
        # Если адрес есть в кэше, то сообщение о превышении количества запросов.
        if cache.get(ip_address):
            return HttpResponse('Too many requests', status=429)

        # Установка лимита запросов
        cache.set(ip_address, True, 2)

        response = self.get_response(request)
        return response
