from django.apps import AppConfig

class EquipmentConfig(AppConfig):
    name = 'equipment'

    def ready(self):
        import equipment.signals
        from equipment.scheduler import start
        start()