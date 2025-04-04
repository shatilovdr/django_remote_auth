from django.apps import AppConfig


class FortytwoConfig(AppConfig):
    name = 'fortytwo'
    verbose_name = "42 OAuth2"

    def ready(self):
        from allauth.socialaccount.providers import registry
        from .provider import FortyTwoProvider
        registry.register(FortyTwoProvider)