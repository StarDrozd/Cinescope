from typing import Optional
import datetime
from typing import List, Dict, Any
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

class TestMovie(BaseModel):
    name: str
    imageUrl: str = 'https://example.com/image.png'
    price: int
    description: str
    location: str
    published: bool
    genreId: int

class EditMovie(BaseModel):
    name: Optional[str] = None
    imageUrl: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    location: Optional[str] = None
    published: Optional[bool] = None
    genreId: Optional[int] = None

class ReviewResponse(BaseModel):
    userId: str
    rating: int = Field(ge=0, le=5)
    text: str
    hidden: bool
    createdAt: str
    user: Dict[str, str]

class MovieResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: str
    location: str
    published: bool
    genreId: int
    genre: Dict[str, str]
    createdAt: str
    rating: int

class FindOneMovieResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: str
    published: bool
    genreId: int
    genre: Dict[str, str]
    createdAt: str
    rating: int = Field(ge=0, le=5)
    reviews: Dict[str, str]
    
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

class FindAllMoviesResponse(BaseModel):
    movies: List[MovieResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int

