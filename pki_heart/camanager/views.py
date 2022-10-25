from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required

from .forms import CertificationAuthorityForm
from pki_heart.forms import bulma_render_form, bulma_render_form_submit


@login_required()
def index(request):
    template = loader.get_template('index.html')
    context = {
        'active_section': 'overview'
    }
    return HttpResponse(template.render(context, request))


def authorities(request):
    template = loader.get_template('authorities.html')
    context = {
        'active_section': 'authorities'
    }
    return HttpResponse(template.render(context, request))


def create_authority(request):
    if request.method == 'POST':
        form = CertificationAuthorityForm(request.POST)
        if not form.is_valid():
            return JsonResponse(bulma_render_form_submit(form))
        else:
            return JsonResponse({'success': True, 'redirect': '/ca/authorities'})
    else:
        template = loader.get_template('create-authority.html')
        form = CertificationAuthorityForm()
        context = {
            'active_section': 'authorities',
            'form': bulma_render_form(form),
            'form_id': 'create-authority-form'
        }
        return HttpResponse(template.render(context, request))
