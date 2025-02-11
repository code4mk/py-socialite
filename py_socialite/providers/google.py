import requests
from typing import Dict, Any
from ..exceptions import SocialAuthError
from .base import SocialProvider

class GoogleProvider(SocialProvider):
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_auth_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scope,
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTH_URL}?{query_string}"

    def get_token(self, code: str) -> Dict[str, Any]:
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }

        response = requests.post(self.TOKEN_URL, data=data)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get token: {response.text}")
            
        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.USER_INFO_URL, headers=headers)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get user info: {response.text}")

        user_data = response.json()
        
        return {
            'provider': 'google',
            'id': user_data.get('sub'),
            'email': user_data.get('email'),
            'name': user_data.get('name'),
            'avatar': user_data.get('picture'),
            'raw': user_data
        } 