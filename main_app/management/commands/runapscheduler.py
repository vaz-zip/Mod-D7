import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail
from django.contrib.auth.models import User
from ...models import Post, Category
from datetime import timedelta
from django.utils import timezone


logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():

    now = timezone.now()
    list_week_posts = Post.objects.filter(dateCreation__gte=now - timedelta(days=7))

    for user in User.objects.filter():
        print('\nИмя пользователя:', user)
        print('e-mail пользователя:', user.email)
        list_group_user = user.groups.values_list('name', flat=True)
        print('Состоит в группах:', list(list_group_user))
        list_category_id = list(Category.objects.filter(name__in=list_group_user).values_list('id', flat=True))
        print('id категорий подписки:', list_category_id)
        list_week_posts_user = list_week_posts.filter(postCategory__in=list_category_id)
        print('Список постов, созданных за период:\n', list(list_week_posts_user))
        if list_week_posts_user:
            list_posts = ''
            for post in list_week_posts_user:
                list_posts += f'\n{post}\nhttp://127.0.0.1:8000/news/{post.id}'

            send_mail(
                subject=f'News Portal: посты за прошедшую неделю.',
                message=f'Добрый день, {user}!\n Онакомьтесь с публикациями, появившимися за последние 7 дней:\n{list_posts}',
                from_email='vaz-zip@yandex.ru',
                recipient_list=[user.email, ],
            )




def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")


        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00")
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
