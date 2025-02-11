from typing import Dict, Any
import requests
from ..exceptions import SocialAuthError
from .base import SocialProvider

class FacebookProvider(SocialProvider):
    AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"
    TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    USER_INFO_URL = "https://graph.facebook.com/v18.0/me"

    def get_auth_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scope
        }
        
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTH_URL}?{query_string}"

    def get_token(self, code: str) -> Dict[str, Any]:
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri
        }

        response = requests.get(self.TOKEN_URL, params=data)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get token: {response.text}")
            
        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        params = {
            'fields': 'id,name,email,picture',
            'access_token': access_token
        }
        
        response = requests.get(self.USER_INFO_URL, params=params)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get user info: {response.text}")

        user_data = response.json()
        
        return {
            'provider': 'facebook',
            'id': user_data.get('id'),
            'email': user_data.get('email'),
            'name': user_data.get('name'),
            'avatar': user_data.get('picture', {}).get('data', {}).get('url'),
            'raw': user_data
        }