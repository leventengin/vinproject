from django.apps import AppConfig


class KuryeConfig(AppConfig):
    name = 'kurye'
    def ready(self):
        import kurye.signals