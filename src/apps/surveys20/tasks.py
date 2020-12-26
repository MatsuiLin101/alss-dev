import os
import csv
import pyminizip
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage

from config import celery_app as app
from apps.surveys20.models import FarmerStat, Survey
from apps.surveys20.export import SurveyRelationGeneratorFactory, StatisticsExporter


@app.task
def async_export_108(email):
    try:
        factory = SurveyRelationGeneratorFactory(excludes={'note__icontains': '無效戶'})
        row_generator = factory.export_generator()

        file_name = f"108_Full_Export_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        file_path = f'{file_name}.csv'
        zip_path = f'{file_name}.zip'

        with open(file_path, 'w+', encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in row_generator:
                writer.writerow(row)

        pyminizip.compress(file_path, "", zip_path, settings.ZIP_PROTECT_SECRET, 5)

        with open(zip_path, 'rb') as zip_file:
            mail = EmailMessage(
                '108調查表匯出完成',
                '請下載附件後解壓縮查看調查表',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            mail.attach('108調查表.zip', zip_file.read(), 'application/zip')
            mail.send()
    except Exception as e:
        EmailMessage(
            '108調查表匯出失敗',
            f"系統發生錯誤，請通知管理員處理。\n{e}",
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ).send()
    finally:
        try:
            os.remove(file_path)
            os.remove(zip_path)
        except Exception:
            pass


@app.task
def async_export_108_statistics(email):
    try:
        exporter = StatisticsExporter()

        file_name = f"108_Statistic_Report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        file_path = f'{file_name}.xlsx'
        zip_path = f'{file_name}.zip'

        exporter(file_path)

        pyminizip.compress(file_path, "", zip_path, settings.ZIP_PROTECT_SECRET, 5)

        with open(zip_path, 'rb') as zip_file:
            mail = EmailMessage(
                '108平台統計結果表式匯出完成',
                '匯出結果如附件',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            mail.attach('108平台統計結果表式.zip', zip_file.read(), 'application/zip')
            mail.send()
    except Exception as e:
        EmailMessage(
            '108平台統計結果表式匯出失敗',
            f"系統發生錯誤，請通知管理員處理。\n{e}",
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ).send()
    finally:
        try:
            os.remove(file_path)
            os.remove(zip_path)
        except Exception:
            pass


@app.task
def async_update_stratify(survey_id):
    survey = Survey.objects.get(id=survey_id)
    if '無效戶' in survey.note:
        FarmerStat.objects.filter(survey=survey).delete()
        return f"Delete {survey} FarmerStat, it's been mark as invalid farmer."
    else:
        stratify = FarmerStat.get_stratify(survey)
        FarmerStat.objects.update_or_create(
            survey=survey,
            defaults={
                'stratify': stratify
            }
        )
        return f'Classify survey {survey} to stratify {stratify}.'
