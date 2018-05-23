from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator


User = get_user_model()

chValidator = RegexValidator("[^0-9a-zA-Z]", _('Please Input Chinese Only'))


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label=_('Account'))
    first_name = forms.CharField(label=_('First Name'), validators=[chValidator])
    last_name = forms.CharField(label=_('Last Name'), validators=[chValidator])
    reset_email = forms.EmailField(label=_('Reset Email'), required=False)

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'reset_email',
            'first_name',
            'last_name',
        ]


class UserLoginForm(forms.Form):
    username = forms.CharField(label=_('Account'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    # This field just for identity validate inactive error in views.py
    is_active = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=True)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_('Your account or password is incorrect'))
            if not user.is_active:
                self.cleaned_data['is_active'] = False
                raise forms.ValidationError(_('Please activate your account'))

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label=_('Account'))
    email = forms.EmailField(label=_('Email'))
    first_name = forms.CharField(label=_('First Name'), validators=[chValidator])
    last_name = forms.CharField(label=_('Last Name'), validators=[chValidator])
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Confirm Password'))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'last_name',
            'first_name',
            'password',
            'password2'
        ]

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError(_('Password must match'))
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(_('This email has already been registered'))
        return email


class UserResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Confirm Password'), required=True)

    class Meta:
        model = User
        fields = [
            'password',
            'password2'
        ]

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError(_('Password must match'))
        return password


class SendMailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = User
        fields = [
            'email'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if not email_qs.exists():
            raise forms.ValidationError(_('This email is not exist'))
        return email
