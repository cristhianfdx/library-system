import logging
import os

from django.apps import AppConfig
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class BooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"

    def ready(self):
        from django.db.utils import OperationalError

        User = get_user_model()
        username = os.getenv("DEFAULT_ADMIN_USER", "admin")
        email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username, email=email, password=password
                )
                logger.info("Usuario admin creado automáticamente.")
            else:
                logger.info("Usuario admin ya existe.")
        except OperationalError:
            pass
