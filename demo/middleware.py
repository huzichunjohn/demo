import time
from metrology import Metrology

http_ok = Metrology.counter('http.ok')
http_err = Metrology.counter('http.err')
response_time = Metrology.histogram('request.time')

class RequestMetricsMiddleware(object):
    def process_request(self, request):
        request._start_time = int(time.time() * 1000)

    def process_response(self, request, response):
        response_time.update(int(time.time() * 1000) - request._start_time)
        if 200 <= response.status_code < 400:
            http_ok.increment()
        else:
            http_err.increment()
        return response

    def process_exception(self, request, exception):
        http_err.increment()
