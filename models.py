from pydantic import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional


class User(BaseModel, UserMixin):
    id: Optional[int] = None
    name: str
    password_hash: Optional[str] = None
    email: str

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
