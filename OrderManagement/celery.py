"""
This is where you can configure celery tasks, like schedule
"""

from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderManagement.settings')
CELERY_BROKER_URL = "redis://redis:6379"

app = Celery('order')
app.config_from_object('django.conf:settings')
app.conf.broker_url = CELERY_BROKER_URL


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from api.tasks import check_failed_orders, check_idle_orders
    interval = 60 * 5  # 5 min
    sender.add_periodic_task(interval,
                             check_failed_orders.s(),
                             name='Check Scheduled Tasks(interval={})'.format(interval))
    interval = 60  # 1 min
    sender.add_periodic_task(interval,
                             check_idle_orders.s(),
                             name='Check Scheduled Tasks(interval={})'.format(interval))
