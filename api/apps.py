from django.apps import AppConfig


class Api(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    """DRF User App Config"""

    verbose_name = "Authorization & Authentication"

    def ready(self):
        """
        Register signals
        Call update_user_settings() to update the user setting as per
        django configurations
        Returns
        -------
        Author: Himanshu Shankar (https://himanshus.com)
        """
        
        #import api.signals
        pass 
