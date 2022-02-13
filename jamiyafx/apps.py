from django.apps import AppConfig


class JamiyafxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jamiyafx"

    def ready(self):
        try:
            import jamiyafx.signals  # noqa F401
        except ImportError:
            pass
