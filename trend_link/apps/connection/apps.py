from django.apps import AppConfig


class ConnectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.connection"

    def ready(self) -> None:
        import apps.connection.signals
