from django.apps import AppConfig
import redis


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'


red = redis.Redis(
    host='redis-17188.c8.us-east-1-2.ec2.cloud.redislabs.com',
    port=17188,
    password='jmPxy4TYtYlmyOzdt0B1EBbYU8pOKEPm'
)
