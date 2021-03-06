import django_otp
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, BACKEND_SESSION_KEY
from django.utils.translation import ugettext_lazy as _
from django_otp.admin import OTPAdminAuthenticationForm, OTPAdminSite


class PersonAuthenticationForm(OTPAdminAuthenticationForm):
    username = forms.EmailField(
        label=_("Adresse email"), widget=forms.EmailInput(attrs={"autofocus": True})
    )

    password = forms.CharField(
        label=_("Mot de passe"), strip=False, widget=forms.PasswordInput
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"username": self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        if len(self.device_choices(self.user_cache)) > 0:
            self.clean_otp(self.get_user())

        return self.cleaned_data


class APIAdminSite(OTPAdminSite):
    login_form = PersonAuthenticationForm
    site_header = "France insoumise"
    site_title = "France insoumise"
    index_title = "Administration"

    def __init__(self, name=OTPAdminSite.name):
        super(APIAdminSite, self).__init__(name=name)

    def has_permission(self, request):
        return (
            super(OTPAdminSite, self).has_permission(request)
            and request.session[BACKEND_SESSION_KEY]
            == "agir.people.backend.PersonBackend"
            and (
                request.user.is_verified()
                or not django_otp.user_has_device(request.user)
            )
        )

    def each_context(self, request):
        return {
            "production_colors": settings.ADMIN_PRODUCTION,
            **super().each_context(request),
        }
