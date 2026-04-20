def test_jwt_token_creation():
    from src.api.schemas.auth import Token
    token = Token(access_token="test.token.here", token_type="bearer")
    assert token.access_token is not None
    assert token.token_type == "bearer"

def test_user_creation():
    from src.api.models.user import User
    user = User(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"
