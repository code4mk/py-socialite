import requests
from typing import Dict, Any
from ..exceptions import SocialAuthError
from .base import SocialProvider

class MicrosoftProvider(SocialProvider):
    """
    Microsoft provider class.
    """

    AUTH_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
    TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
    USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"

    def get_auth_url(self) -> str:
        """
        Get the authorization URL for Microsoft authentication.
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scope,
            'response_mode': 'query'
        }
        
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTH_URL}?{query_string}"

    def get_token(self, code: str) -> Dict[str, Any]:
        """
        Get the access token for Microsoft authentication.
        """
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
        """
        Get the user information for Microsoft authentication.
        """

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.USER_INFO_URL, headers=headers)
        
        if response.status_code != 200:
            raise SocialAuthError(f"Failed to get user info: {response.text}")

        user_data = response.json()
        
        return {
            'provider': 'microsoft',
            'id': user_data.get('id'),
            'email': user_data.get('userPrincipalName'),
            'name': user_data.get('displayName'),
            'avatar': None,  # Microsoft Graph API doesn't provide avatar in basic profile
            'raw': user_data
        }
