import os
from typing import Union, List, Tuple, Iterator
from ._load import load_assetstudio

load_assetstudio()

from .ObjectReader import ObjectReader
from AssetStudio import (
    AssetsManager as AssetsManagerCS,
    ObjectReader as ObjectReaderCS,
    ClassIDType as ClassIDTypeCS,
    TextAsset as TextAssetCS,
    Texture2D as Texture2DCS,
    AssetBundle as AssetBundleCS,
)


class AssetsManager:
    _assetsmanager: AssetsManagerCS

    def __init__(
        self, inp: Union[str, bytes, bytearray, List[Union[bytes, bytearray]]]
    ) -> None:
        self._assetsmanager = AssetsManagerCS()
        self.load_value(inp)

    def load_value(self, data: Union[str, bytes, bytearray]) -> None:
        if isinstance(data, str) or (
            isinstance(data, list) and all(isinstance(x, str) for x in data)
        ):
            self._assetsmanager.LoadFiles(data)
        elif isinstance(data, (bytes, bytearray)):
            self._assetsmanager.LoadFromMemory(data)
        elif isinstance(data, list):
            for x in data:
                self._assetsmanager.load_value(x)

    def load_files(self, files: Union[str, List[str]]) -> None:
        self._assetsmanager.LoadFiles(files)

    def load_from_memory(self, data: Union[str, bytes, bytearray]) -> None:
        self._assetsmanager.LoadFromMemory(data)

    def get_objects(self) -> Iterator[ObjectReader]:
        for assetsFile in self._assetsmanager.assetsFileList:
            for objectInfo in assetsFile.m_Objects:
                objectReader = ObjectReader(assetsFile.reader, assetsFile, objectInfo)
                yield objectReader

    def get_container(self) -> Iterator[Tuple[str, ObjectReader]]:
        for obj in self.get_objects():
            if obj.type == ClassIDTypeCS.AssetBundle:
                ab = AssetBundleCS(obj)
                for key, value in ab.m_Container.items():
                    yield key, ObjectReader.from_ObjectReaderCS(value.asset)
