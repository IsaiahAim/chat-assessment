# middleware.py

from django.http import HttpResponseForbidden

from client.cache import get_client_key


class ApiKeyMiddleware:
    EXCLUDED_PATHS = [
        '/api/v1/doc/',
        '/api/schema/',
        '/api/v1/clients/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with '/api/'
        if request.path.startswith('/api/') and not any(request.path.startswith(path) for path in self.EXCLUDED_PATHS):
            api_key = request.headers.get('x-api-key')

            if not api_key:
                return HttpResponseForbidden('API key is required for this request.')

            if not get_client_key(api_key):
                return HttpResponseForbidden('Invalid API Key')

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

