from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .forms import LoginForm
from pki_heart.forms import bulma_render_form, bulma_render_form_submit_error


@login_required
def index(request):
    template = loader.get_template('accounts/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def login(request):
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect', '/ca')
        form = LoginForm(request.POST)
        if not form.is_valid():
            return JsonResponse(bulma_render_form_submit_error(form))
        else:
            # perform authentication here
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'success': True, 'redirect': redirect_url})
            else:
                form.add_error('username', 'Incorrect username or password')
                return JsonResponse(bulma_render_form_submit_error(form))
    else:
        redirect_url = request.GET.get('redirect', '/ca')
        form = LoginForm()
        form.fields['redirect'].initial = redirect_url
        template = loader.get_template('accounts/login.html')
        context = {
            'form_id': 'login-form',
            'form': bulma_render_form(form),
        }
        return HttpResponse(template.render(context, request))


def logout(request):
    auth_logout(request)
    return JsonResponse({'success': True})