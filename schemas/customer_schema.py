from pydantic import BaseModel, Field, EmailStr


class CustomerCreate(BaseModel):
    first_name: str = Field(
        min_length=1,
        max_length=50,
        pattern=r"^[A-Za-z]+(?: [A-Za-z]+)*$"
    )
    last_name: str = Field(
        min_length=1,
        max_length=50,
        pattern=r"^[A-Za-z]+(?: [A-Za-z]+)*$"
        )
    email: EmailStr = Field(max_length=100)
    phone_number: str = Field(
        min_length=10,
        max_length=10,
        pattern=r"^\d{10}$"
    )
    address: str = Field(min_length=1, max_length=150)

    model_config = {
        "extra": "forbid"
    }
class CustomerUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        pattern=r"^[A-Za-z]+(?: [A-Za-z]+)*$"
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        pattern=r"^[A-Za-z]+(?: [A-Za-z]+)*$"
    )

    phone_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        pattern=r"^\d{10}$"
    )

    email: EmailStr | None = Field(
        default=None,
        max_length=100
    )

    address: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )

    model_config = {
        "extra": "forbid"
    }