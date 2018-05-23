from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth import(
    authenticate,
    login,
    logout,
    get_user_model
)
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import (
    UserLoginForm,
    UserRegisterForm,
    SendMailForm,
    UserResetPasswordForm,
    UserEditForm
)
from .models import ActivationProfile, ResetPasswordProfile, ResetEmailProfile

User = get_user_model()


def resend_mail_view(request):
    form = SendMailForm(request.POST or None)
    template = 'resend_mail.html'
    content = {
        'form': form,
        'mail_sent': request.session.get('mail_sent', 'False')
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        ActivationProfile.objects.create(user=user)
        content['mail_sent'] = True
        return render(request, template, content)
    return render(request, template, content)


def edit_info_view(request):
    usr = User.objects.filter(username=request.user).first()
    data = dict()
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usr)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = UserEditForm(instance=usr)
    context = {'form': form}
    data['html_form'] = render_to_string('edit_info.html', context, request=request)
    return JsonResponse(data)


def login_view(request):
    form = UserLoginForm(request.POST or None)
    content = {
        'form': form
    }
    template = 'login.html'

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        request.session['mail_sent'] = False
        return redirect('index')

    if form.errors:
        is_active = form.cleaned_data.get('is_active')
        if is_active is False:
            content['resend_email'] = True

    return render(request, template, content)


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    template = 'register.html'
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        request.session['mail_sent'] = True
        return redirect('accounts:resend-mail')

    context = {
        "form": form
    }
    return render(request, template, context)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def reset_email_view(request, key=None):
    q = ResetEmailProfile.objects.filter(key=key)

    if q.exists() and q.count() == 1:
        activation = q.first()
        if not activation.expired:
            user = activation.user
            user.email = activation.new_email
            user.is_active = True
            user.save()
            activation.expired = True
            activation.save()
        return redirect('accounts:login')
    else:
        raise Http404


def user_activate(request, key=None, *args, **kwargs):
    q = ActivationProfile.objects.filter(key=key)

    if q.exists() and q.count() == 1:
        activation = q.first()
        if not activation.expired:
            user = activation.user
            user.is_active = True
            user.save()
            activation.expired = True
            activation.save()
        return redirect('accounts:login')
    else:
        raise Http404


def forget_password_view(request):
    form = SendMailForm(request.POST or None)
    content = {
        "form": form,
        "mail_sent": True
    }
    template = 'forget_password.html'

    if form.is_valid():
        email = form.cleaned_data.get('email')
        usr = User.objects.filter(email=email).first()
        ResetPasswordProfile.objects.create(user=usr)
        content['mail_sent'] = False
        return render(request, template, content)
    return render(request, template, content)


def reset_password_view(request, key=None):
    template = 'reset_password.html'
    form = UserResetPasswordForm(request.POST or None)
    q = ResetPasswordProfile.objects.filter(key=key)
    context = {
        "valid_link": False,
        "form": form,
        "mail_sent": True
    }
    if q.exists() and q.count() == 1:
        reset = q.first()
        if not reset.expired:
            context['valid_link'] = True

    if request.method == 'POST':
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = reset.user
            user.set_password(password)
            user.save()
            reset.expired = True
            reset.save()
            context['mail_sent'] = False
            return render(request, template, context)

    return render(request, template, context)
