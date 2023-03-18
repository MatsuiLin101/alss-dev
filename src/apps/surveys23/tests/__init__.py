import pytest
from django.test import TestCase


@pytest.mark.s22
class TestCase(TestCase):
    pass


def setup_fixtures():
    from django.core.management import call_command
    call_command("loaddata", "fixtures/surveys23/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/city-town-code.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/contract.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/education-level.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/farm-related-business.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/farmer-work-day.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/gender.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/income-range.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/lack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/land-status.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/unit.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/land-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/life-style.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/loss.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/management-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/market-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/month.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/product.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/refuse-reason.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/relationship.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/work-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys23/subsidy-result.yaml", verbosity=0)
