from django.apps import AppConfig

class AnchorConfig(AppConfig):
    name = "app"

    def ready(self):
        from polaris.integrations import register_integrations
        
        from .integrations import (
            toml_contents,
        )

        register_integrations(
            toml = toml_contents,
        )