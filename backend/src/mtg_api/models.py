from datetime import date

from sqlalchemy import Unicode, UnicodeText
from sqlmodel import Field, Relationship, SQLModel


class Set(SQLModel, table=True):
    __tablename__ = "sets"

    id: int | None = Field(default=None, primary_key=True)
    scryfall_id: str = Field(max_length=36, unique=True, index=True)
    code: str = Field(max_length=8, unique=True, index=True)
    name: str = Field(sa_type=Unicode(200))
    set_type: str = Field(max_length=50)
    released_at: date | None = None

    printings: list["Printing"] = Relationship(back_populates="set")

class OracleCard(SQLModel, table=True):
    __tablename__ = "oracle_cards"

    id: int | None = Field(default=None, primary_key=True)
    scryfall_oracle_id: str = Field(max_length=36, unique=True, index=True)
    name: str = Field(sa_type=Unicode(200), index=True)
    mana_cost: str | None = Field(default=None, max_length=100)
    type_line: str = Field(sa_type=Unicode(200))
    oracle_text: str | None = Field(default=None, sa_type=UnicodeText)
    cmc: float | None = Field(default=None, index=True)
    colors: str | None = Field(default=None, max_length=5)
    color_identity: int = Field(default=0)
    commander_legal: bool = Field(default=False, index=True)