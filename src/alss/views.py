from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from surveys18.models import FarmRelatedBusiness, ManagementType


class Index(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['farm_related_businesses'] = FarmRelatedBusiness.objects.all()
        context['management_types'] = ManagementType.objects.all()

        return context

