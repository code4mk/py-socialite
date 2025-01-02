
# Folder Structure

```
py-socialite/
├── py_socialite/
│   ├── __init__.py         # Version and package info
│   ├── exceptions.py       # Custom exceptions
│   ├── config.py           # Provider configurations
│   ├── social_auth_service.py  # Main service class
│   └── providers/
│       ├── base.py         # Abstract base provider
│       └── google.py       # Google implementation
├── setup.py                # Package setup
└── deploy.sh              # Deployment script
```