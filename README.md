A Python package for OAuth authentication with various social providers, inspired by Laravel Socialite.

## Installation

```bash
pip install py-socialite
```

## Configuration

Create a configuration file (e.g., socialite.py) with your OAuth credentials:

```python
# socialite.py

SOCIAL_PROVIDERS = {
    'google': {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'redirect_uri': 'your-callback-url',
        'scope': 'openid email profile'
    },
    'github': {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'redirect_uri': 'your-callback-url',
        'scope': 'read:user user:email'
    },
    'dropbox': {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'redirect_uri': 'your-callback-url'
    },
    'x': {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'redirect_uri': 'your-callback-url',
        'scope': 'tweet.read users.read follows.read offline.access'
    },
    'linkedin': {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'redirect_uri': 'your-callback-url',
        'scope': 'openid profile email'
    },
    'facebook': {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'redirect_uri': 'your-callback-url',
        'scope': 'email public_profile'
    },
    'microsoft': {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'redirect_uri': 'your-callback-url',
        'scope': 'openid email profile User.Read'
    }
}
```
Set the configuration path in your environment:

```bash
export SOCIALITE_CONFIG_PATH="modules.common.config.socialite"

# or add it to your .env file
SOCIALITE_CONFIG_PATH='modules.common.config.socialite'
```

## Usage

```python
from py_socialite.socialite import Socialite

# Initialize Socialite
socialite = Socialite()

# Get authorization URL
auth_url = socialite.provider('google').get_auth_url()

# After callback, get user info
user = socialite.provider('google').get_user(code)
```

## Error Handling

The package raises `SocialAuthError` for any authentication issues.

```python
try:
    user = socialite.provider('google').get_user(code)
except SocialAuthError as e:
    print(f"Authentication failed: {str(e)}")
```

## Project Structure

```bash
py-socialite/
├── py_socialite/
│   ├── __init__.py         # Version and package info
│   ├── exceptions.py       # Custom exceptions
│   ├── config.py           # Provider configurations
│   ├── socialite.py        # Main service class
│   └── providers/
│       ├── base.py         # Abstract base provider
│       └── google.py       # Google implementation
├── setup.py                # Package setup
└── deploy.sh              # Deployment script
```

## Requirements

- python 3.10+
- requests
- python-dotenv

## support providers

- google
- github
- dropbox
- x
- facebook
- microsoft
- linkedin


## Response sample data

```bash
{
    "provider": "google",
    "id": "1234567890",
    "email": "example@example.com",
    "name": "John Doe",
    "avatar": "https://example.com/avatar.jpg",
    "raw": {
        .....
    }
}
```

## Resources

- [How to use py-socialite on django - medium](https://code4mk.medium.com/py-socialite-implement-on-django-and-drf-2b2531bdb6e9)
- [How to use py-socialite on fastapi - medium](https://code4mk.medium.com/py-socialite-implement-on-fastapi-b1d585c7f915)


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
