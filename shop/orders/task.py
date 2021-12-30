from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from shop.settings import EMAIL_HOST_USER


@shared_task()
def order_created(order_id):
    """Задача отправки email - при успешном оформлении заказа."""
    order = Order.objects.get(id=order_id)
    subject = f'Order {order_id}'
    message = f'Заказ {order.first_name} успешно оформлен, номер вашего заказа №{order_id}'
    mail_send = send_mail(subject,
                          message,
                          EMAIL_HOST_USER,
                          [order.email])
    return mail_send