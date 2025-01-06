from typing import Dict, Any
from py_socialite.providers.google import GoogleProvider
from py_socialite.providers.github import GitHubProvider
from py_socialite.providers.dropbox import DropboxProvider
from py_socialite.providers.x import XProvider
from py_socialite.providers.linkedin import LinkedInProvider
from py_socialite.exceptions import SocialAuthError
from py_socialite.providers.facebook import FacebookProvider
from py_socialite.providers.microsoft import MicrosoftProvider
from importlib import import_module
from dotenv import load_dotenv
import os

class Socialite:
    """Main class for handling social authentication."""
    
    def __init__(self):
        """Initialize Socialite with supported providers."""
        self._providers = {
            'google': GoogleProvider,
            'github': GitHubProvider,
            'dropbox': DropboxProvider,
            'x': XProvider,
            'linkedin': LinkedInProvider,
            'facebook': FacebookProvider,
            'microsoft': MicrosoftProvider
        }
        self.selected_provider = None
        
        # Load environment variables
        load_dotenv()
        
        # Get config path from environment variable
        config_path = os.getenv('SOCIALITE_CONFIG_FILE', '')
        
        # Dynamically import the config
        try:
            self.config_module = import_module(config_path)
            self.social_providers = getattr(self.config_module, 'SOCIAL_PROVIDERS', {})
        except ImportError:
            raise SocialAuthError(f"Could not import config from {config_path}")
        except AttributeError:
            raise SocialAuthError(f"SOCIAL_PROVIDERS not found in {config_path}")

    def provider(self, provider_name: str) -> 'Socialite':
        """
        Select and configure a social provider.
        
        Args:
            provider_name: Name of the social provider to use
            
        Returns:
            self: Returns the instance for method chaining
        """
        provider_class = self._providers.get(provider_name)
        if not provider_class:
            supported_providers = ", ".join(self._providers.keys())
            raise SocialAuthError(f"Provider '{provider_name}' not supported. Supported providers are: {supported_providers}")

        config = self.social_providers.get(provider_name)
        if not config:
            raise SocialAuthError(f"Configuration for {provider_name} not found")

        self.selected_provider = provider_class(config)
        return self

    def get_auth_url(self) -> str:
        """Get the authorization URL for the selected provider."""
        if not self.selected_provider:
            raise SocialAuthError("No provider selected. Call provider() first.")
            
        return self.selected_provider.get_auth_url()

    def get_user(self, code: str) -> Dict[str, Any]:
        """
        Get user information from the provider.
        
        Returns:
            Dict containing user information
        """
        if not self.selected_provider:
            raise SocialAuthError("No provider selected. Call provider() first.")

        # Get token from authorization code
        token_data = self.selected_provider.get_token(code)
        access_token = token_data.get('access_token')
        
        if not access_token:
            raise SocialAuthError("No access token received")

        # Get user information
        return self.selected_provider.get_user_info(access_token)
 