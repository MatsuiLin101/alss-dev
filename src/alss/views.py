from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from surveys18.models import (
    FarmRelatedBusiness,
    ManagementType,
    LandType,
    IncomeRange,
    MarketType,
    AgeScope,
    Gender,
    Lack,
)


class Index(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['farm_related_businesses'] = FarmRelatedBusiness.objects.all()
        context['management_types'] = ManagementType.objects.all()
        context['land_types'] = LandType.objects.all()
        context['income_ranges'] = IncomeRange.objects.all()
        context['market_types'] = MarketType.objects.all()
        context['genders'] = Gender.objects.all()
        context['population_age_scopes'] = AgeScope.objects.filter(group=2)
        context['hire_age_scopes'] = AgeScope.objects.filter(group=1)
        context['lacks'] = Lack.objects.all()
        return context

