"""
Vercel serverless function handler for Django WSGI application.
This file serves as the entry point for Vercel's serverless functions.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farmsetu_weather.settings")

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize Django application
application = get_wsgi_application()

# Vercel expects a handler function that receives a request object
def handler(request):
    """
    Handle incoming requests for Vercel serverless function.
    This function adapts Vercel's request format to WSGI.
    """
    from io import BytesIO
    
    # Extract request information
    method = getattr(request, 'method', 'GET')
    path = getattr(request, 'path', '/')
    query_string = getattr(request, 'query_string', '') or ''
    headers = getattr(request, 'headers', {})
    body = getattr(request, 'body', b'') or b''
    
    # Build WSGI environment dictionary
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', headers.get('Content-Type', '')),
        'CONTENT_LENGTH': str(len(body)) if body else '',
        'SERVER_NAME': headers.get('host', headers.get('Host', 'localhost')).split(':')[0],
        'SERVER_PORT': headers.get('host', headers.get('Host', 'localhost')).split(':')[1] if ':' in headers.get('host', headers.get('Host', '')) else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(body) if body else BytesIO(),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add HTTP headers to environ (convert to HTTP_* format)
    for key, value in headers.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key_upper}'] = value
    
    # Response storage
    response_data = []
    status_code = 200
    response_headers = []
    
    def start_response(status, headers):
        """WSGI start_response callback."""
        nonlocal status_code, response_headers
        status_code = int(status.split()[0])
        response_headers = headers
    
    # Call the WSGI application
    try:
        result = application(environ, start_response)
        
        # Collect response body
        for data in result:
            if isinstance(data, bytes):
                response_data.append(data)
            elif isinstance(data, str):
                response_data.append(data.encode('utf-8'))
        
        # Close the result if it has a close method
        if hasattr(result, 'close'):
            result.close()
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Return error response
        from vercel import Response
        return Response(
            f'Internal Server Error: {str(e)}'.encode('utf-8'),
            status=500,
            headers={'Content-Type': 'text/plain; charset=utf-8'}
        )
    
    # Build response
    from vercel import Response
    response_headers_dict = dict(response_headers)
    response_body = b''.join(response_data)
    
    return Response(
        response_body,
        status=status_code,
        headers=response_headers_dict
    )

