from typing import Dict, Any
from ..exceptions import SocialAuthError
from .base import SocialProvider
import requests

class DropboxProvider(SocialProvider):
    AUTH_URL = "https://www.dropbox.com/oauth2/authorize"
    TOKEN_URL = "https://api.dropboxapi.com/oauth2/token"
    USER_INFO_URL = "https://api.dropboxapi.com/2/users/get_current_account"

    def get_auth_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'token_access_type': 'offline',  # To get refresh token
        }
        
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTH_URL}?{query_string}"

    def get_token(self, code: str) -> Dict[str, Any]:
        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
        }

        response = requests.post(self.TOKEN_URL, data=data)

        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get token: {response.text}")
            
        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.post(self.USER_INFO_URL, headers=headers)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get user info: {response.text}")
            
        user_data = response.json()
        
        return {
            'provider': 'dropbox',
            'id': str(user_data.get('account_id')),
            'name': user_data.get('name', {}).get('display_name'),
            'email': user_data.get('email'),
            'raw': user_data
        }