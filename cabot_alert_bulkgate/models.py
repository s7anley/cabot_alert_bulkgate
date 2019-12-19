from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from os import environ as env

from django.conf import settings
from django.template import Context, Template

import logging
import requests
import json

logger = logging.getLogger(__name__)

bulk_gate_endpoint = "https://portal.bulkgate.com/api/1.0/simple/transactional"
sms_template = "Service {{ service.name }} reporting {{ service.overall_status }} status: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}"

class BulkgateSMS(AlertPlugin):
    name = "Bulkgate SMS"
    slug = "cabot_alert_bulkgate"
    author = ""

    def send_alert(self, service, users, duty_officers):
        # No need to call to sent, that things are resolved
        if service.overall_status != service.CRITICAL_STATUS:
            return

        app_id = env.get('BULKGATE_APP_ID')
        app_token  = env.get('BULKGATE_APP_TOKEN')

        duty_officers_list = list(duty_officers)
        users_to_notify = list(users) if not duty_officers_list else duty_officers_list

        mobiles = BulkGateUserData.objects.filter(user__user__in=users_to_notify)
        mobiles = [m.prefixed_phone_number for m in mobiles if m.phone_number]

        c = Context({
            'service': service,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
        })

        message = Template(sms_template).render(c)
        for mobile in mobiles:
            try:
                resp = requests.post(bulk_gate_endpoint, data={
                    'application_id': app_id,
                    'application_token': app_token,
                    'number': mobile,
                    'text': message,
                })

                if not resp.ok:
                    logger.exception('Error sending bulkgate sms %s' % resp.text)

            except Exception, e:
                logger.exception('Error sending bulkgate sms: %s' % e)

class BulkGateUserData(AlertPluginUserData):
    name = "Bulkgate Plugin"
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    def save(self, *args, **kwargs):
        if str(self.phone_number).startswith('+'):
            self.phone_number = self.phone_number[1:]
        return super(BulkGateUserData, self).save(*args, **kwargs)

    @property
    def prefixed_phone_number(self):
        return '+%s' % self.phone_number

    def serialize(self):
        return {
            "phone_number": self.phone_number
        }
