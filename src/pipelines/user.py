
from src.models.base import get_session
from src.models.user import UserModel
from src.schemas.user import UserSchema, UserResponseSchema

def create_user(user: UserSchema) -> UserResponseSchema:
    user_state = UserModel.fill(**user.dict())

    with get_session() as session:
        session.add(user_state)
        session.commit()
    
    return UserResponseSchema(
        data=user,
        success=True,
        message="User created"
    )
