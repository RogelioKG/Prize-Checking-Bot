# standard library
from abc import ABC, abstractmethod
import json
import pickle
from typing import Any


# 使用策略模式 (Strategy Pattern) 設計 Accessor 


class Serializer(ABC):
    @abstractmethod
    def read(self, filepath: str) -> dict[str, Any]:
        pass
    @abstractmethod
    def write(self, obj: dict[str, Any], filepath: str) -> None:
        pass


class Json(Serializer):
    def read(self, filepath: str) -> dict[str, Any]:
        with open(filepath, mode="r", encoding="utf-8") as json_file:
            obj = json.load(json_file)
        return obj
    def write(self, obj: dict[str, Any], filepath: str) -> None:
        with open(filepath, mode="w", encoding="utf-8") as json_file:
            json.dump(obj, json_file)


class Pickle(Serializer):
    def read(self, filepath: str) -> dict[str, Any]:
        with open(filepath, mode="rb") as pkl_file:
            obj = pickle.load(pkl_file)
        return obj
    def write(self, obj: dict[str, Any], filepath: str) -> None:
        with open(filepath, mode="wb") as pkl_file:
            pickle.dump(obj, pkl_file)


class Accessor():
    def __init__(self, accessor: Serializer):
        self.accessor = accessor
    def read(self, filepath: str):
        return self.accessor.read(filepath)
    def write(self, obj: dict[str, Any], filepath: str) -> None:
        return self.accessor.write(obj, filepath)


if __name__ == "__main__":
    pass