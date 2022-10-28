import sys

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.db.models import F
from django.urls import reverse

from .forms import CertificationAuthorityForm, NewCACertForm, EditCACertForm
from .models import CertificationAuthority, CACertificate
from pki_heart.forms import bulma_render_form, bulma_render_form_submit_error, bulma_render_submit_error
from pki_heart import utils


@login_required
def index(request):
    template = loader.get_template('camanager/index.html')
    context = {
        'active_section': 'overview'
    }
    return HttpResponse(template.render(context, request))


@login_required
def authorities(request):
    template = loader.get_template('camanager/authorities.html')
    query = CertificationAuthority.objects.filter(owner=request.user)
    authorities = []
    for x in query:
        authorities.append({
            'id': x.id,
            'name': x.name
            })
    context = {
        'active_section': 'authorities',
        'authorities': authorities
    }
    return HttpResponse(template.render(context, request))


@login_required
def create_authority(request):
    if request.method == 'POST':
        form = CertificationAuthorityForm(request.POST)
        if not form.is_valid():
            return JsonResponse(bulma_render_form_submit_error(form))
        else:
            try:
                authority = CertificationAuthority(owner = request.user, name = form.cleaned_data['name'],
                    description = form.cleaned_data['description'])
                authority.save()
            except IntegrityError:
                form.add_error('name', 'Authority with the same name already exists.')
                return JsonResponse(bulma_render_form_submit_error(form))

            return JsonResponse({'success': True, 'redirect': reverse('show_authority', args=[authority.id])})
    else:
        template = loader.get_template('camanager/create-authority.html')
        form = CertificationAuthorityForm()
        context = {
            'active_section': 'authorities',
            'form': bulma_render_form(form),
            'form_id': 'create-authority-form'
        }
        return HttpResponse(template.render(context, request))


@login_required
def show_authority(request, authority_id):
    if request.method != 'GET':
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    try:
        authority = CertificationAuthority.objects.get(id = authority_id, owner = request.user)
    except CertificationAuthority.DoesNotExist:
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    template = loader.get_template('camanager/show-authority.html')
    query = CACertificate.objects.filter(owner = request.user, certification_authority = authority)
    certificates = []
    for x in query:
        certificates.append({
            'id': x.id,
            'name': x.name
            })
    context = {
        'active_section': 'authorities',
        'authority': authority,
        'certificates': certificates
    }
    return HttpResponse(template.render(context, request))


@login_required
def edit_authority(request, authority_id):
    try:
        authority = CertificationAuthority.objects.get(id = authority_id, owner = request.user)
    except CertificationAuthority.DoesNotExist:
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    if request.method == 'POST':
        form = CertificationAuthorityForm(request.POST)
        if not form.is_valid():
            return JsonResponse(bulma_render_form_submit_error(form))
        else:
            data = form.cleaned_data
            try:
                authority.name = data['name']
                authority.description = data['description']
                authority.save()
            except IntegrityError:
                form.add_error('name', 'Authority with the same name already exists.')
                return JsonResponse(bulma_render_form_submit_error(form))

            return JsonResponse({'success': True, 'redirect': reverse('show_authority', args=[authority.id])})
    else:
        template = loader.get_template('camanager/edit-authority.html')
        form = CertificationAuthorityForm(initial={
            'name': authority.name,
            'description': authority.description
            })
        context = {
            'active_section': 'authorities',
            'authority': authority,
            'form': bulma_render_form(form),
            'form_id': 'edit-authority-form'
        }
        return HttpResponse(template.render(context, request))


@login_required
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


@login_required
def create_authority_ca_cert(request, authority_id):
    try:
        authority = CertificationAuthority.objects.get(id = authority_id, owner = request.user)
    except CertificationAuthority.DoesNotExist:
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    if request.method == 'POST':
        form = NewCACertForm(request.POST)
        if not form.is_valid():
            return JsonResponse(bulma_render_form_submit_error(form))
        else:
            data = form.cleaned_data
            # TODO: parse subject
            subject = ''
            # TODO: check private_key_algorithm
            try:
                certificate = CACertificate(owner = request.user, certification_authority = authority,
                    name = data['name'],
                    description = data['description'], allow_issue = data['allow_issue'],
                    subject = subject, private_key_algorithm = data['private_key_algorithm'],
                    issued_by_certificate = None)
                certificate.save()
            except IntegrityError:
                form.add_error('name', 'Certificate with the same name already exists.')
                return JsonResponse(bulma_render_form_submit_error(form))
            return JsonResponse({'success': True, 'redirect': reverse('show_authority_ca_cert', args=[authority.id, certificate.id])})
    else:
        template = loader.get_template('camanager/create-authority-ca-cert.html')
        form = NewCACertForm(initial={'allow_issue': True})
        context = {
            'active_section': 'authorities',
            'authority': authority,
            'form_id': 'create-authority-ca-cert',
            'form': bulma_render_form(form)
        }
        return HttpResponse(template.render(context, request))


@login_required
def show_authority_ca_cert(request, authority_id, certificate_id):
    try:
        authority = CertificationAuthority.objects.get(id = authority_id, owner = request.user)
    except CertificationAuthority.DoesNotExist:
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    try:
        certificate = CACertificate.objects.get(id = certificate_id, certification_authority = authority, owner = request.user)
    except CACertificate.DoesNotExist:
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    template = loader.get_template('camanager/show-authority-ca-cert.html')
    context = {
        'active_section': 'authorities',
        'authority': authority,
        'certificate': certificate
    }
    return HttpResponse(template.render(context, request))


@login_required
def edit_authority_ca_cert(request, authority_id, certificate_id):
    try:
        authority = CertificationAuthority.objects.get(id = authority_id, owner = request.user)
    except CertificationAuthority.DoesNotExist:
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    try:
        certificate = CACertificate.objects.get(id = certificate_id, certification_authority = authority, owner = request.user)
    except CACertificate.DoesNotExist:
        return utils.HttpErrorResponse(404, 'Resource not found', request)

    if request.method == 'POST':
        form = EditCACertForm(request.POST)
        if not form.is_valid():
            return JsonResponse(bulma_render_form_submit_error(form))
        else:
            data = form.cleaned_data
            try:
                certificate.name = data['name']
                certificate.description = data['description']
                certificate.allow_issue = data['allow_issue']
                certificate.save()
            except IntegrityError:
                form.add_error('name', 'Certificate with the same name already exists.')
                return JsonResponse(bulma_render_form_submit_error(form))

            return JsonResponse({'success': True, 'redirect': reverse('show_authority_ca_cert', args=[authority.id, certificate.id])})
    else:
        template = loader.get_template('camanager/edit-authority-ca-cert.html')
        form = EditCACertForm(initial={
            'name': certificate.name,
            'description': certificate.description,
            'allow_issue': certificate.allow_issue
            })
        context = {
            'active_section': 'authorities',
            'authority': authority,
            'certificate': certificate,
            'form': bulma_render_form(form),
            'form_id': 'edit-authority-form'
        }
        return HttpResponse(template.render(context, request))

@login_required
def delete_authority_ca_cert(request, authority_id):
    return HttpResponse('DELETE CERT')

