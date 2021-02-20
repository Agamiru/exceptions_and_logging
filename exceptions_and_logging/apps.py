from django.apps import AppConfig


class ExceptionsAndLoggingConfig(AppConfig):
    name = 'exceptions_and_logging'

    def ready(self):
        from django.conf import settings
        from .settings import EXCEPTION_HANDLER
        rest_framework_settings = getattr(settings, "REST_FRAMEWORK", None)
        if rest_framework_settings is not None:
            rest_framework_settings["EXCEPTION_HANDLER"] = EXCEPTION_HANDLER
        else:
            setattr(settings, "REST_FRAMEWORK", {"EXCEPTION_HANDLER": EXCEPTION_HANDLER})








