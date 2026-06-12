from typing import Optional
import datetime
import re
from typing import List
from pydantic import BaseModel, Field, field_validator
from constants.roles import Roles

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: List[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        use_enum_values = True  # 👈 ЭТО преобразует Enum в значения при .dict()
        json_encoders = {       # 👈 ЭТО для .json() метода (тоже полезно)
            Roles: lambda v: v.value
        }
class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    @classmethod
    def validate_created_at(cls, value: str) -> str:
        """Проверяет формат ISO 8601 (поддерживает Z на конце)"""
        try:
            # Заменяем Z на +00:00 для корректного парсинга
            normalized = value.replace('Z', '+00:00')
            datetime.datetime.fromisoformat(normalized)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value