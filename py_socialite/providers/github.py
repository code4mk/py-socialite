import requests
from typing import Dict, Any
from ..exceptions import SocialAuthError
from .base import SocialProvider

class GitHubProvider(SocialProvider):
    AUTH_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_INFO_URL = "https://api.github.com/user"

    def get_auth_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope
        }
        
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTH_URL}?{query_string}"

    def get_token(self, code: str) -> Dict[str, Any]:
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
        }
        
        headers = {
            'Accept': 'application/json'
        }

        response = requests.post(self.TOKEN_URL, data=data, headers=headers)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get token: {response.text}")
            
        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/json'
        }
        
        # Get user profile
        response = requests.get(self.USER_INFO_URL, headers=headers)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get user info: {response.text}")

        user_data = response.json()
        
        # Get user email (if not public)
        email_response = requests.get(f"{self.USER_INFO_URL}/emails", headers=headers)
        email = user_data.get('email')
        
        if not email and email_response.status_code == 200:
            emails = email_response.json()
            primary_email = next((e for e in emails if e.get('primary')), None)
            if primary_email:
                email = primary_email.get('email')
        
        return {
            'provider': 'github',
            'id': str(user_data.get('id')),
            'email': email,
            'name': user_data.get('name'),
            'avatar': user_data.get('avatar_url'),
            'raw': user_data
        }
