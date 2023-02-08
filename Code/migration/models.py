from datetime import date as date_type
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, validator


class AttributeTypes(Enum):
    string = "String"
    string_list = "StringList"
    numeric = "Numeric"
    numeric_list = "NumericList"
    date = "Date"
    date_list = "DateList"
    datetime = "DateTime"
    datetime_list = "DateTimeList"


class TitleBaseModel(BaseModel):
    title: Optional[str] = Field(default=None)

    @validator("title")
    def title_not_empty_string(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        return value

    def __hash__(self) -> int:
        return (self.title or "").__hash__()


class Entry(TitleBaseModel):
    date: Optional[date_type] = None
    namespace: Optional[str] = Field(
        default=None,
        description="Used to create multiple Entries with the same title, "
        "e.g. when using empty titles for all entries.",
    )

    def __hash__(self) -> int:
        return (
            super().__hash__()
            ^ (self.date or "").__hash__()
            ^ (self.namespace or "").__hash__()
        )

    class Config:
        extra = "forbid"


class Document(TitleBaseModel):
    namespace: Optional[str] = Field(
        default=None,
        description="Used to create multiple Documents with the same title. "
        "We recommend using the original filename in this field, enabeling re-usage "
        'of document titles "combinations" e.g. pdf/docx.',
    )

    def __hash__(self) -> int:
        return super().__hash__() ^ (self.namespace or "").__hash__()

    class Config:
        extra = "forbid"


class Attribute(BaseModel):
    name: str
    type: AttributeTypes = Field(
        ...,
        description="For the regular (not list) types, only a single value can be "
        "assigned to a entry, multiple values will result in a undefined result.",
    )
    value: Union[int, float, datetime, date_type, str]

    @validator("value")
    def type_value_validation(cls, value: Any, values: dict[str, Any]):
        requierd_type = values.get("type", None)
        if requierd_type is None:
            return None

        if value is None:
            raise ValueError('Requierd field "value" was not found or null')

        value_type = str(type(value).__name__)
        if requierd_type in [AttributeTypes.datetime, AttributeTypes.datetime_list]:
            if not isinstance(value, datetime):
                raise TypeError(f'Field value was "{value_type}" not type "datetime"')

        elif requierd_type in [AttributeTypes.date, AttributeTypes.date_list]:
            if isinstance(value, datetime):
                value = value.date()

            if not isinstance(value, date_type):
                raise TypeError(f'Field value was "{value_type}" not type "date"')

        elif requierd_type in [AttributeTypes.numeric, AttributeTypes.numeric_list]:
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f'Field value was "{value_type}" not type "int" or "float"'
                )

        elif requierd_type in [AttributeTypes.string, AttributeTypes.string_list]:
            if isinstance(value, (str, int, float)):
                value = str(value)

            if not isinstance(value, str):
                raise TypeError(f'Field value was "{value_type}" not type "str"')

        else:
            raise TypeError(f'Field value was type "{value_type}"')

        return value

    def __hash__(self) -> int:
        if self.type in [
            AttributeTypes.date,
            AttributeTypes.datetime,
            AttributeTypes.numeric,
            AttributeTypes.string,
        ]:
            return self.name.__hash__() ^ self.type.__hash__()

        return self.name.__hash__() ^ self.type.__hash__() ^ self.value.__hash__()

    class Config:
        extra = "forbid"


class Tag(BaseModel):
    title: str
    entry_attributes: set[Attribute] = Field(default_factory=set)

    def __hash__(self) -> int:
        return self.title.__hash__()

    class Config:
        extra = "forbid"


class FileImportModel(BaseModel):
    section: Optional[str] = Field(
        default=None,
        description="Excplisitly find/set the *title* of the section.",
    )
    file_name: Optional[str] = Field(
        default=None,
        description="Replaces the file **name** which will be shown on documentVersion.",
    )
    document: Optional[Document] = Field(
        default=None,
    )
    entry: Optional[Entry] = Field(
        default=None,
    )
    classification_tags: dict[str, set[Tag]] = Field(
        default_factory=dict,
        description="Entries get grouped, i.e. unless separated by entry-namespace "
        "tags will be merged onto entries with the same section & entry-title.",
    )

    class Config:
        extra = "forbid"
