from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required

from .forms import CertificationAuthorityForm
from .models import CertificationAuthority
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
    items = CertificationAuthority.objects.all()
    authorities = []
    for x in items:
        authorities.append({
            'id': x.id,
            'name': x.name
            })
    context = {
        'active_section': 'authorities',
        'authorities': authorities
    }
    return HttpResponse(template.render(context, request))


def create_authority(request):
    if request.method == 'POST':
        form = CertificationAuthorityForm(request.POST)
        if not form.is_valid():
            return JsonResponse(bulma_render_form_submit(form))
        else:
            authority = CertificationAuthority(name = form.cleaned_data['name'],
                description = form.cleaned_data['description'])
            authority.save()
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


def delete_authority(request):
    ids = []
    for x in request.POST.getlist('ids'):
        try:
            v = int(x)
            if v > 0:
                ids.append(v)
        except:
            pass
    if len(ids) == 0:
        return JsonResponse({'success': False, 'errors': [{'error_text': 'empty list of IDs'}]})
    else:
        for x in ids:
            try:
                authority = CertificationAuthority.objects.get(id = x)
                authority.delete()
            except CertificationAuthority.DoesNotExist:
                # ignore this error
                pass
        return JsonResponse({'success': False})

