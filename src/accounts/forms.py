from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from django.utils.translation import ugettext as _

User = get_user_model()


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label=_('帳號'))
    first_name = forms.CharField(label=_('姓'))
    last_name = forms.CharField(label=_('名'))
    reset_email = forms.EmailField(label=_('更改信箱'), required=False)

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
    username = forms.CharField(label=_('帳號'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('密碼'))
    # This field just for identity validate inactive error in views.py
    is_active = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=True)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_('您輸入的帳號或密碼不正確，請重試'))
            if not user.is_active:
                self.cleaned_data['is_active'] = False
                raise forms.ValidationError(_('請先啟用您的帳戶'))

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label=_('帳號'))
    email = forms.EmailField(label=_('電子信箱'))
    first_name = forms.CharField(label=_('姓'))
    last_name = forms.CharField(label=_('名'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('密碼'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('確認密碼'))

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
            raise forms.ValidationError(_('密碼不符'))
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(_('這個信箱已經被使用過了'))
        return email


class UserResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label=_('密碼'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('確認密碼'), required=True)

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
            raise forms.ValidationError(_('密碼不符'))
        return password


class SendMailForm(forms.Form):
    email = forms.EmailField(label=_('電子信箱'))

    class Meta:
        model = User
        fields = [
            'email'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if not email_qs.exists():
            raise forms.ValidationError(_('這個信箱不存在'))
        return email
