from django.apps import AppConfig


class VisitlogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visitlogs'

    def ready(self):
        import visitlogs.signals