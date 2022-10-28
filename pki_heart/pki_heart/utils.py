from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.template import loader



def HttpErrorResponse(code, message, request):
    template = loader.get_template('error.html')
    context = {
        'message': message,
        'error_name': 'Error'
    }
    if code == 404:
        context['error_name'] = '404 Not Found'
        return HttpResponseNotFound(template.render(context, request))
    else:
        return HttpResponseBadRequest(template.render(context, request))


def supported_private_key_algorithms():
    return [{
        'id': 'rsa:2048',
        'label': 'RSA 2048 bits'
    }, {
        'id': 'rsa:1024',
        'label': 'RSA 1024 bits'
    }, {
        'id': 'ec:prime256v1',
        'label': 'EC prime256v1 / secp256r1 / NIST P-256'
    }, {
        'id': 'ec:secp384r1',
        'label': 'EC secp384r1 / NIST P-384'
    }]