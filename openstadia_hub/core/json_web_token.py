from dataclasses import dataclass

import jwt
from fastapi import HTTPException, status

from .config import settings


@dataclass
class JsonWebToken:
    jwt_access_token: str
    auth0_issuer_url: str = f"https://{settings.auth0_domain}/"
    auth0_audience: str = settings.auth0_audience
    algorithm: str = "RS256"
    jwks_uri: str = f"{auth0_issuer_url}.well-known/jwks.json"

    def validate(self):
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(
                self.jwt_access_token
            ).key
            payload = jwt.decode(
                self.jwt_access_token,
                jwt_signing_key,
                algorithms=self.algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
                leeway=10
            )
        except jwt.exceptions.PyJWKClientError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to verify credentials",
            )
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bad credentials"
            )
        return payload
