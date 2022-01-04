from typing import Any
from ._load import load_assetstudio

load_assetstudio()

from System import Enum
import AssetStudio
from AssetStudio import (
    ObjectReader as ObjectReaderCS,
    ClassIDType,
)


class ObjectReader:
    _objectreader: ObjectReaderCS

    def __init__(
        self, reader: bytes, assetsfile: "AssetsFile", objectinfo: "ObjectInfo"
    ) -> None:
        self._objectreader = ObjectReaderCS(reader, assetsfile, objectinfo)

    @staticmethod
    def from_ObjectReaderCS(obj: "ObjectReaderCS") -> "ObjectReader":
        return ObjectReader(obj.reader, obj.assetsfile, obj.objectinfo)

    @property
    def typeName(self) -> str:
        return Enum.GetName(ClassIDType, self._objectreader.type)

    def toClassType(self):
        return getattr(AssetStudio, self.typeName)(self._objectreader)

    def export(self, path) -> Any:
        pass  # TODO

    def __getattr__(self, key: str) -> Any:
        return getattr(self._objectreader, key)
