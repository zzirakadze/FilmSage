from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db


class UserActions:
    def __init__(self):
        """
        Queries for user actions
        """
        self.get_user_via_email_query = """
            SELECT id, name, surname, username FROM user WHERE email = :email
            """

        self.update_user_query = """
        UPDATE user SET name = :name, surname = :surname, username = :username WHERE id = :user_id
            """

    def get_user_by_email(self, email: str):
        try:
            user = db.session.execute(
                db.text(self.get_user_via_email_query), {"email": email}
            ).fetchone()
            return {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "username": user.username,
            }
        except SQLAlchemyError as e:
            print(f"Database query failed: {e}")
            return f"'error': {e}"
        except Exception as e:
            if "NoneType" in str(e):
                print("User cant found with provided email")
            return None

    def update_user(self, name: str, surname: str) -> bool:
        try:
            db.session.execute(
                db.text(self.update_user_query),
                {
                    "name": name,
                    "surname": surname,
                },
            )
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database query failed: {e}")
            return False
        except Exception as e:
            print(f"Exception: {e}")
            return False
