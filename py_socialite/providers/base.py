from abc import ABC, abstractmethod
from typing import Dict, Any

class SocialProvider(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client_id = config.get('client_id')
        self.client_secret = config.get('client_secret')
        self.redirect_uri = config.get('redirect_uri')

    @abstractmethod
    def get_auth_url(self) -> str:
        pass

    @abstractmethod
    def get_token(self, code: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        pass 