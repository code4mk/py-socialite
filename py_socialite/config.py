from typing import Dict, Any

SOCIAL_PROVIDERS: Dict[str, Dict[str, Any]] = {
    'google': {
        'client_id': '',
        'client_secret': '',
        'redirect_uri': 'http://localhost:8011/api/v1/user/social-auth/google/callback'
    }
}