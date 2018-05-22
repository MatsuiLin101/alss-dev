from django.contrib import admin

from .models import (ActivationProfile,
                     UserInformation,
                     ResetPasswordProfile,
                     ResetEmailProfile,
                     AbstractProfile)


admin.site.register(ActivationProfile)
admin.site.register(UserInformation)
admin.site.register(ResetPasswordProfile)
admin.site.register(ResetEmailProfile)
admin.site.register(AbstractProfile)
