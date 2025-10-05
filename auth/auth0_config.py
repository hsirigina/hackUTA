"""Auth0 configuration and authentication handlers."""
import os
from typing import Optional, Dict, Any
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv
import requests

load_dotenv()


class Auth0Config:
    """Auth0 configuration manager."""

    def __init__(self):
        self.domain = os.getenv('AUTH0_DOMAIN')
        self.client_id = os.getenv('AUTH0_CLIENT_ID')
        self.client_secret = os.getenv('AUTH0_CLIENT_SECRET')
        self.callback_url = os.getenv('AUTH0_CALLBACK_URL', 'http://localhost:8501/callback')
        self.app_url = os.getenv('APP_URL', 'http://localhost:8501')

        # Validate required config
        if not all([self.domain, self.client_id, self.client_secret]):
            raise ValueError(
                "Missing Auth0 configuration. Please set AUTH0_DOMAIN, "
                "AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET in .env file"
            )

        # Auth0 URLs
        self.authorize_url = f'https://{self.domain}/authorize'
        self.token_url = f'https://{self.domain}/oauth/token'
        self.userinfo_url = f'https://{self.domain}/userinfo'
        self.logout_url = f'https://{self.domain}/v2/logout'

    def get_oauth_session(self, state: Optional[str] = None, token: Optional[Dict] = None) -> OAuth2Session:
        """Create an OAuth2 session for Auth0."""
        return OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.callback_url,
            scope='openid profile email',
            state=state,
            token=token
        )

    def get_authorization_url(self, force_login: bool = False) -> tuple[str, str]:
        """Get the authorization URL and state for login."""
        session = self.get_oauth_session()

        # Add prompt=login to force user to re-authenticate (useful after logout)
        extra_params = {}
        if force_login:
            extra_params['prompt'] = 'login'

        authorization_url, state = session.create_authorization_url(
            self.authorize_url,
            **extra_params
        )
        return authorization_url, state

    def exchange_code_for_token(self, authorization_response: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        session = self.get_oauth_session()
        token = session.fetch_token(
            self.token_url,
            authorization_response=authorization_response
        )
        return token

    def get_user_info(self, token: Dict[str, Any]) -> Dict[str, Any]:
        """Get user information from Auth0."""
        session = self.get_oauth_session(token=token)
        user_info = session.get(self.userinfo_url).json()
        return user_info

    def get_user_metadata(self, user_id: str, management_token: str) -> Dict[str, Any]:
        """
        Get user metadata including role and relationships.
        Requires a Management API token.
        """
        url = f'https://{self.domain}/api/v2/users/{user_id}'
        headers = {'Authorization': f'Bearer {management_token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            return {
                'role': user_data.get('app_metadata', {}).get('role', 'driver'),
                'supervisor_id': user_data.get('app_metadata', {}).get('supervisor_id'),
                'supervised_users': user_data.get('app_metadata', {}).get('supervised_users', [])
            }
        return {}

    def get_logout_url(self, return_to: Optional[str] = None) -> str:
        """Get the logout URL."""
        return_url = return_to or self.app_url
        return f'{self.logout_url}?client_id={self.client_id}&returnTo={return_url}'


# Global config instance
auth0_config = Auth0Config()
