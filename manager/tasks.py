from datetime import date
from celery import shared_task
from celery.schedules import crontab
from django.contrib.auth.models import User
from django.core.mail import send_mail
from celery.task import periodic_task


@periodic_task(run_every=crontab(minute=0, hour=12))
def check_users_tasks():

    for user in User.objects.all():
        send_notification.delay(user.id)


@shared_task()
def send_notification(user_id):
    user = User.objects.get(id=user_id)
    todays_task = user.tasks.filter(due_date=date.today())
    if len(todays_task)>0 and user.email:
        message = 'Tasks on today:\n' + '\n'.join([t.title for t in todays_task])
        send_mail(
            'Tasks',
            message,
            'vladislav.lipsky@gmail.com',
            [user.email, ],
            fail_silently=False,
        )