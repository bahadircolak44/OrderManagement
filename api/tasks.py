import logging
from datetime import datetime, timedelta

from OrderManagement import celery_app
from api.db_models.order import Order
from utils.publish import publish
from django.utils import timezone as _timezone

logger = logging.getLogger(__name__)


@celery_app.task
def check_idle_orders(*args, **kwargs):
    """
    Checks the orders in every min that was not able to published in time, and try to publish again.
    """
    order_list = Order.objects.filter(status=Order.Status.IDLE).order_by(
        '-created_at').values('id', 'foods__restaurants__id')
    for order in order_list:
        try:
            publish({'id': order.get('order')}, f"order-{order.get('foods__restaurants__id')}")
        except:
            # It is not important, task will be run min later
            pass


@celery_app.task
def check_failed_orders(*args, **kwargs):
    """
    Checks the orders in every 5 min that was not able to consumed in time, and make their status Failed.
    """
    Order.objects.filter(status__in=[Order.Status.QUEUED, Order.Status.IDLE],
                         created_at__lte=_timezone.now() - timedelta(hours=1)).update(
        status=Order.Status.FAILED)
