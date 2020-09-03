from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from srcode import mail
from config import Config, EmailConfig
import jwt

def generate_confirmation_token(email):
     serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
     return serializer.dumps(email, salt= EmailConfig.PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=EmailConfig.PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email
