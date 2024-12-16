from django.db import connection
from django.utils.deprecation import MiddlewareMixin

class CloseDBConnectionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        connection.close()
        return response
