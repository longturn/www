from django.http import JsonResponse
from longturn.meta.models import Server
import json
import socket
import urllib

def meta(request):
    # Erase unresponsive servers
    Server.remove_old()

    # Build the list of all active servers
    response = {
        'servers': [server.json() for server in Server.objects.all()],
        'status': 'ok'
    }
    return JsonResponse(response)

def sanitize_url(request, url):
    """Performs some validation of incoming URLs"""

    # Parse it
    url = urllib.parse.urlparse(url)
    if url.scheme != 'fc21':
        raise Exception('URL scheme must be fc21')
    # Leave credentials untouched
    # Make sure we have a host name
    if url.hostname == None:
        raise Exception('No hostname specified')
    # Make sure we have a port
    if url.port == None:
        raise Exception('No port specified')
    # The rest of the URL is unused

    # Check that the host matches the IP (prevent someone from erasing all
    # servers)
    try:
        ip = request.META['REMOTE_ADDR']
        addrinfo = socket.getaddrinfo(url.hostname, url.port or 5556,
                                      0, 0, socket.IPPROTO_TCP)
        for entry in addrinfo:
            if entry[-1][0] == ip:
                break # ok!
        else:
            # No way someone can contact the remote server using this host name
            raise Exception(f"Host name {url.hostname} doesn't match your IP {ip}")
    except OSError:
        # Most likely the domain doesn't exist
        raise Exception(f"Could not resolve host {url.hostname}")

    # Standardize
    return urllib.parse.urlunparse(url)

def announce(request):
    # Allow only POST requests
    if request.method != 'POST':
        return JsonResponse({'status': 'error',
                             'message': 'Only POST is allowed'},
                            status=405)

    # Parse the contents and try to add to the db...
    try:
        payload = json.loads(request.body)

        # Do some validation of the URL
        url = sanitize_url(request, payload['url'])

        # Insert into the DB
        server = Server()
        server.url = url
        server.id = payload.get('id', '')
        server.message = payload.get('message', '')
        server.patches = payload.get('patches', '')
        server.capability = payload.get('capability', '')
        server.version = payload.get('version', '')
        server.state = payload.get('state', '')
        server.available = payload.get('available', 0)
        server.humans = payload.get('humans', 0)
        server.save()

        return JsonResponse({'status': 'ok'})
    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error',
                             'message': 'JSON parse error'},
                            status=400)
    except Exception as e:
        return JsonResponse({'status': 'error',
                             'message': str(e)},
                            status=400)

def leave(request):
    # Allow only POST requests
    if request.method != 'POST':
        return JsonResponse({'status': 'error',
                             'message': 'Only POST is allowed'},
                            status=405)

    # Parse the contents and try to remove from the db
    try:
        payload = json.loads(request.body)

        # Do some validation of the URL
        url = sanitize_url(request, payload['url'])

        # Remove from the DB
        Server.objects.get(url=url).delete()

        return JsonResponse({'status': 'ok'})
    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error',
                             'message': 'JSON parse error'},
                            status=400)
    except Exception as e:
        return JsonResponse({'status': 'error',
                             'message': str(e)},
                            status=400)
