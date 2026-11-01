from datetime import date

from sqlalchemy import Unicode, UnicodeText
from sqlmodel import Field, Relationship, SQLModel

SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


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

    printings: list["Printing"] = Relationship(back_populates="oracle_card")


class Printing(SQLModel, table=True):
    __tablename__ = "printings"

    id: int | None = Field(default=None, primary_key=True)
    scryfall_id: str = Field(max_length=36, unique=True, index=True)
    set_id: int = Field(foreign_key="sets.id", index=True)
    set: Set = Relationship(back_populates="printings")
    oracle_card_id: int = Field(foreign_key="oracle_cards.id", index=True)
    oracle_card: OracleCard = Relationship(back_populates="printings")

    collector_number: str = Field(max_length=16)
    rarity: str = Field(max_length=20)
    lang: str = Field(max_length=5)
    frame: str = Field(max_length=16)
    artist: str | None = Field(default=None, sa_type=Unicode(200))
    flavor_text: str | None = Field(default=None, sa_type=UnicodeText)
    image_url: str | None = Field(default=None, max_length=500)

    has_nonfoil: bool = Field(default=False)
    has_foil: bool = Field(default=False)
    has_etched: bool = Field(default=False)
