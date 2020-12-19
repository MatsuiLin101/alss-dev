import csv
import io
import zipfile

from django.conf import settings
from django.core.mail import EmailMessage

from config import celery_app as app
from apps.surveys19.export import SurveyRelationGeneratorFactory


@app.task
def async_export_107(email):
    try:
        factory = SurveyRelationGeneratorFactory(excludes={'note__icontains': '無效戶'})
        row_generator = factory.export_generator()

        sio = io.StringIO()
        writer = csv.writer(sio)

        for row in row_generator:
            writer.writerow(row)

        mail = EmailMessage(
            '107調查表匯出完成',
            '請下載附件後解壓縮查看調查表',
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )
        mail.attach('107調查表.csv', sio.getvalue(), 'text/csv')
        mail.send()
    except Exception as e:
        EmailMessage(
            '107調查表匯出失敗',
            f"系統發生錯誤，請通知管理員處理。\n{e}",
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ).send()
