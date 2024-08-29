from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    def ready(self):
        # Đảm bảo rằng signals được import khi ứng dụng sẵn sàng
      import myapp.signals
