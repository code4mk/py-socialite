from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union

class SocialProvider(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client_id = config.get('client_id')
        self.client_secret = config.get('client_secret')
        self.redirect_uri = config.get('redirect_uri')
        self.scope = self._parse_scope(config.get('scope', []))

    def _parse_scope(self, scope: Union[str, List[str]]) -> str:
        """
        Parse scope from config into a space-separated string.
        Accepts either a list of scopes or a space-separated string.
        """
        if isinstance(scope, list):
            return ' '.join(scope)
        return str(scope)

    @abstractmethod
    def get_auth_url(self) -> str:
        pass

    @abstractmethod
    def get_token(self, code: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        pass 