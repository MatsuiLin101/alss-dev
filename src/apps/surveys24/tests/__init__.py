import pytest
from django.test import TestCase


@pytest.mark.s24
class TestCase(TestCase):
    pass


def setup_fixtures():
    from django.core.management import call_command

    call_command("loaddata", "fixtures/surveys24/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/city-town-code.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/contract.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/education-level.yaml", verbosity=0)
    call_command(
        "loaddata", "fixtures/surveys24/farm-related-business.yaml", verbosity=0
    )
    call_command("loaddata", "fixtures/surveys24/farmer-work-day.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/gender.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/income-range.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/lack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/land-status.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/unit.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/land-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/life-style.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/loss.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/management-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/market-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/month.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/product.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/refuse-reason.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/relationship.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/work-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/apply-result.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys24/apply-method.yaml", verbosity=0)
