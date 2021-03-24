from django.apps import AppConfig


class SocialappConfig(AppConfig):
    name = 'socialApp'

    def ready(self):
        import socialApp.signals