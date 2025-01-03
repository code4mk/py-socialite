from typing import Dict, Any
from ..exceptions import SocialAuthError
from .base import SocialProvider
import requests
from urllib.parse import urlencode

class LinkedInProvider(SocialProvider):
    AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
    TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    USER_INFO_URL = "https://api.linkedin.com/v2/userinfo"

    def get_auth_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'openid profile email',
            'state': 'state'
        }
        
        return f"{self.AUTH_URL}?{urlencode(params)}"

    def get_token(self, code: str) -> Dict[str, Any]:
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }

        response = requests.post(self.TOKEN_URL, data=data)
        print(response.json())

        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get token: {response.text}")
            
        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Get user info from the OpenID userinfo endpoint
        response = requests.get(self.USER_INFO_URL, headers=headers)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get user info: {response.text}")

        user_data = response.json()
        
        return {
            'provider': 'linkedin',
            'id': user_data.get('sub'),
            'email': user_data.get('email'),
            'name': user_data.get('name'),
            'avatar': user_data.get('picture'),
            'raw': user_data
        }