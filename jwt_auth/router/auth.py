from ninja import Router
from jwt_auth.schemas import (
    AuthSchema,
    BoolSignal,
    Token,
    Error,
    OneInputToken
)
from jwt_auth.models import User
from jwt_auth.utils import (
    Hasher,
    JWTMiddleware
)


router = Router()


@router.post('/token/pair', response={200: Token, 401: Error})
def token_obtain_pair(request, auth: AuthSchema):
    """사용자의 email과 password를 입력받아 JWT를 발급합니다.

    Args:
        auth (AuthSchema): {email: str, password: str}
    """
    user_filter = User.objects.filter(email=auth.email)

    if user_filter.exists():
        user = user_filter.first()
        if Hasher.check_user_is_allowed(auth.password, user):
            return 200, JWTMiddleware.get_all_new_tokens(user.id)

    return 401, {
        'code': 401,
        'message': '올바르지 않은 계정입니다.'
    }


@router.post('/token/refresh', response={200: Token, 401: Error})
def refresh_token(request, token: OneInputToken):

    new_token = JWTMiddleware.decode_token(token.token)

    if new_token:
        return 200, Token(
            access_token=new_token,
            refresh_token=token.token,
        )

    return 401, {
        'code': 401,
        'message': '올바르지 않은 토큰'
    }


@router.post('/token/verify', response={200: BoolSignal})
def token_verify(request, token: OneInputToken):
    return 200, {'bool': JWTMiddleware.verify_token(token.token)}
