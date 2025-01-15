from django.apps import AppConfig


class AiAgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_agents'

    def ready(self):
        print("[DEBUG] AI signal connected.")

        import ai_agents.signals