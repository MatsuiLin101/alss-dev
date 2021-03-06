from . import TestCase, setup_fixtures
from apps.surveys19.models import (
    Survey,
    LandArea,
    LandType,
    LandStatus,
)


class LandAreaTestCase(TestCase):
    """
    models: LandArea, Survey
    reference models : s19-land-type.yaml, s19-land-status.yaml, s19-unit.yaml, s19-product-type.yaml
    data: s19-test-landarea.yaml, s19-test-survey.yaml
    main: LandArea associate other models, the one farmer has many land types/status.
    """

    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_land_area(self):
        survey_id = Survey.objects.get(id=3)
        land_type_a = LandType.objects.get(id=2)
        land_status_a = LandStatus.objects.get(id=2)

        land_area_list_before_size = len(LandArea.objects.all())

        # new value
        LandArea.objects.create(
            survey=survey_id, type=land_type_a, status=land_status_a, value=70
        )

        land_area_list_after_size = len(LandArea.objects.all())
        self.assertEqual(land_area_list_after_size, land_area_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        land_area_list = LandArea.objects.filter(survey__id=1)
        self.assertEqual(land_area_list.count(), 0)

    def test_survey_delete_all(self):
        land_type_list_before_size = len(LandType.objects.all())
        land_status_list_before_size = len(LandStatus.objects.all())
        Survey.objects.all().delete()
        land_area_list = LandArea.objects.all()
        land_type_list_after_size = len(LandType.objects.all())
        land_status_list_after_size = len(LandStatus.objects.all())

        self.assertEqual(len(land_area_list), 0)
        self.assertEqual(land_type_list_after_size, land_type_list_before_size)
        self.assertEqual(land_status_list_after_size, land_status_list_before_size)
