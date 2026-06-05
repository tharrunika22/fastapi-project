from app.features.auth.repository import get_user_by_email

def authenticate_user(db, email, password):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if user.password != password:
        return None

    return user