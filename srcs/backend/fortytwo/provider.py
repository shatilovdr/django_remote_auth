
from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter

class FortyTwoAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('url')

    def get_avatar_url(self):
        return self.account.extra_data.get('image_url')

    def to_str(self):
        return self.account.extra_data.get('displayname', self.account.extra_data.get('login'))

class FortyTwoOAuth2Adapter(OAuth2Adapter):
    provider_id = 'fortytwo'
    access_token_url = 'https://api.intra.42.fr/oauth/token'
    authorize_url = 'https://api.intra.42.fr/oauth/authorize'
    profile_url = 'https://api.intra.42.fr/v2/me'

    def complete_login(self, request, app, token, **kwargs):
        import requests
        headers = {'Authorization': f'Bearer {token.token}'}
        resp = requests.get(self.profile_url, headers=headers)
        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)

class FortyTwoProvider(OAuth2Provider):
    id = 'fortytwo'
    name = '42'
    account_class = FortyTwoAccount
    oauth2_adapter_class = FortyTwoOAuth2Adapter  # Set the adapter here

    def get_default_scope(self):
        return ['public']

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return {
            'email': data.get('email'),
            'username': data.get('login'),
            'name': data.get('displayname'),
        }

    def extract_email_addresses(self, data):
        ret = []
        email = data.get('email')
        if email:
            ret.append(EmailAddress(email=email, verified=True, primary=True))
        return ret

provider_classes = [FortyTwoProvider]
