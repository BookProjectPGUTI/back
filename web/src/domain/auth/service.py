from jwt import PyJWT, InvalidTokenError

from src.config.auth import AUTH_CONFIG
from src.domain.auth.exception import INVALID_CREDENTIALS


class JWT:
    jwt = PyJWT(
        {
            'verify_signature': True, 'verify_aud': False, 'verify_iat': False, 'verify_exp': True, 'verify_nbf': False,
            'verify_iss': False, 'verify_sub': True, 'verify_jti': True, 'verify_at_hash': False, 'require_aud': False,
            'require_iat': False, 'require_exp': True, 'require_nbf': False, 'require_iss': False, 'require_sub': True,
            'require_jti': True, 'require_at_hash': False, 'leeway': 99999,
        }
    )

    @classmethod
    def encode(cls, claims: dict[str, str | int]) -> str:
        return cls.jwt.encode(claims, AUTH_CONFIG.secret, algorithm=AUTH_CONFIG.algorithm)

    @classmethod
    def decode(cls, token: str) -> dict[str, str | int]:
        try:
            return cls.jwt.decode(token, AUTH_CONFIG.secret, algorithms=[AUTH_CONFIG.algorithm])
        except InvalidTokenError:
            raise INVALID_CREDENTIALS
