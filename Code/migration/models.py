from datetime import date as date_type
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class AttributeTypes(Enum):
    string = "String"
    string_list = "StringList"
    numeric = "Numeric"
    numeric_list = "NumericList"
    date = "Date"
    date_list = "DateList"
    datetime = "Date"
    datetime_list = "DateList"


class TitleBaseModel(BaseModel):
    title: Optional[str] = Field(default=None)

    @validator("title")
    def title_not_empty_string(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        return value


class Entry(TitleBaseModel):
    date: Optional[date_type] = None
    namespace: Optional[str] = Field(
        default=None,
        description="Used to create multiple Entries with the same title, "
        "e.g. when using empty titles for all entries.",
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

    class Config:
        extra = "forbid"


class Attribute(BaseModel):
    name: str
    type: AttributeTypes = Field(
        ...,
        description="For the regular (not list) types, only a single value can be "
        "assigned to a entry, multiple values will result in a undefined result.",
    )
    value: Union[datetime, date_type, int, float, str]

    @root_validator
    def type_value_validation(cls, values: dict[str, Any]) -> dict[str, Any]:
        found_type = values.get("type", None)
        if found_type is None:
            raise ValueError('Requierd field "type" was not found or null')

        found_value = values.get("value", None)
        if found_value is None:
            raise ValueError('Requierd field "value" was not found or null')

        if found_type in [AttributeTypes.datetime, AttributeTypes.datetime_list]:
            if not isinstance(found_value, datetime):
                raise ValueError('Field value was not type "datetime"')

        elif found_type in [AttributeTypes.date, AttributeTypes.date_list]:
            if not isinstance(found_value, date_type):
                raise ValueError('Field value was not type "date"')

        elif found_type in [AttributeTypes.numeric, AttributeTypes.numeric_list]:
            if not isinstance(found_value, (int, float)):
                raise ValueError('Field value was not type "int" or "float"')

        elif found_type in [AttributeTypes.string, AttributeTypes.string_list]:
            if not isinstance(found_value, str):
                raise ValueError('Field value was not type "string"')

        else:
            raise ValueError(f'Field value was type "{type(found_value)!s}')

        return values

    def __hash__(self) -> int:
        return self.name.__hash__()

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
