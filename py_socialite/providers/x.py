from typing import Dict, Any
from ..exceptions import SocialAuthError
from .base import SocialProvider
import requests
import base64

class XProvider(SocialProvider):
    AUTH_URL = "https://x.com/i/oauth2/authorize"
    TOKEN_URL = "https://api.x.com/2/oauth2/token"
    USER_INFO_URL = "https://api.x.com/2/users/me"

    def get_auth_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'tweet.read users.read follows.read offline.access',
            'state': 'state',  # You might want to generate a random state
            'code_challenge': 'challenge',  # Should be generated based on PKCE spec
            'code_challenge_method': 'plain'  # Consider using 'S256' for better security
        }
        
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTH_URL}?{query_string}"

    def get_token(self, code: str) -> Dict[str, Any]:
        # Create credentials string with client_id:client_secret
        credentials = f"{self.client_id}:{self.client_secret}".encode('utf-8')
        base64_credentials = base64.b64encode(credentials).decode('utf-8')

        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'code_verifier': 'challenge',  # Should match the value used to generate code_challenge
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {base64_credentials}'
        }

        response = requests.post(self.TOKEN_URL, data=data, headers=headers)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get token: {response.text}")
            
        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        params = {
            'user.fields': 'id,name,username,profile_image_url'
        }
        
        response = requests.get(
            self.USER_INFO_URL,
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get user info: {response.text}")
            
        user_data = response.json().get('data', {})
        
        return {
            'provider': 'x',
            'id': str(user_data.get('id')),
            'email': None,  # Twitter API v2 doesn't provide email by default
            'name': user_data.get('name'),
            'username': user_data.get('username'),
            'avatar': user_data.get('profile_image_url'),
            'raw': user_data
        } 