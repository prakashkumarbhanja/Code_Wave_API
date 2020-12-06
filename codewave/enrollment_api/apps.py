from django.apps import AppConfig


class EnrollmentApiConfig(AppConfig):
    name = 'enrollment_api'

    def ready(self):
        import enrollment_api.signals