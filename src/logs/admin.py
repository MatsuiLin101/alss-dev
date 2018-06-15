from __future__ import unicode_literals
import logging

from django.contrib import admin
from django.utils.html import format_html

from .models import ReviewLog


class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_object', 'initial_errors', 'current_errors', 'update_datetime', 'colored_msg', 'traceback')
    list_display_links = ('colored_msg', )
    list_filter = ('level', 'user', )
    list_per_page = 10

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)
    colored_msg.short_description = 'Message'

    def traceback(self, instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')


admin.site.register(ReviewLog, StatusLogAdmin)
