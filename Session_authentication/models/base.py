#!/usr/bin/env python3
""" Base module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable, Dict, Any
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA: Dict[str, Dict[str, Any]] = {}

T = TypeVar('T', bound='Base')


class Base:
    """Base class"""

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Base instance"""
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

        if isinstance(self.created_at, str):
            self.created_at = datetime.strptime(self.created_at,
                                                TIMESTAMP_FORMAT)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.strptime(self.updated_at,
                                                TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: T) -> bool:
        """Equality"""
        if not isinstance(other, Base):
            return False
        return self.id == other.id and type(self) == type(other)

    def to_json(self, for_serialization: bool = False) -> Dict[str, Any]:
        """Convert the object a JSON dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith("_"):
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls) -> None:
        """Load all objects from file"""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA.setdefault(s_class, {})

        if not path.exists(file_path):
            return

        with open(file_path, "r") as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls) -> None:
        """Save all objects to file"""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {
            obj_id: obj.to_json(True)
            for obj_id, obj in DATA[s_class].items()
        }

        with open(file_path, "w") as f:
            json.dump(objs_json, f, default=str)

    def save(self) -> None:
        """Save current object"""
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self) -> None:
        """Remove object"""
        s_class = self.__class__.__name__
        if self.id in DATA[s_class]:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Count all objects"""
        s_class = cls.__name__
        return len(DATA.get(s_class, {}))

    @classmethod
    def all(cls) -> List[T]:
        """Return all objects"""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> T:
        """Return one object by ID"""
        s_class = cls.__name__
        return DATA.get(s_class, {}).get(id)

    @classmethod
    def search(cls, attributes: Dict[str, Any] = {}) -> List[T]:
        """Search all objects with matching attributes"""
        s_class = cls.__name__

        def _search(obj: T) -> bool:
            if not attributes:
                return True
            for k, v in attributes.items():
                if getattr(obj, k, None) != v:
                    return False
            return True

        return [obj for obj in DATA.get(s_class, {}).values() if _search(obj)]
