from django.apps import AppConfig

# Configuration class for the 'frontend' Django application.
# This class contains settings that are specific to this app.
class FrontendConfig(AppConfig):
    # Specifies the default type of auto field to use for primary keys.
    # Django uses BigAutoField by default in new projects to allow for a larger number of objects.
    default_auto_field = "django.db.models.BigAutoField"
    # The name attribute sets the full Python path to the application.
    # Django uses this configuration to locate and use the application.
    name = "frontend"
