import os
from typing import Union, List, Tuple, Iterator, Any
from ._load import load_assetstudio, get_class_method

load_assetstudio()

from .ObjectReader import ObjectReader
from AssetStudio import (
    AssetsManager as AssetsManagerCS,
    ObjectReader as ObjectReaderCS,
    ClassIDType as ClassIDTypeCS,
    TextAsset as TextAssetCS,
    Texture2D as Texture2DCS,
    AssetBundle as AssetBundleCS,
    FileType as FileTypeCS,
    FileReader as FileReaderCS,
)
from System.IO import MemoryStream, SeekOrigin
from System import ArgumentException

class AssetsManager:
    # TODO:
    # add files to importFilesHash
    _assetsmanager: AssetsManagerCS

    @staticmethod
    def _load_file(assetsmanager: AssetBundleCS, filereader: FileReaderCS):
        if not (
            isinstance(assetsmanager, AssetsManagerCS)
            and isinstance(filereader, FileReaderCS)
        ):
            raise ValueError("Invalid input types")

        for method in get_class_method(AssetsManagerCS, "LoadFile"):
            try:
                method.Invoke(assetsmanager, [filereader])
                AssetsManager._load_file = (
                    lambda assetsmanager, filereader: method.Invoke(
                        assetsmanager, [filereader]
                    )
                )
                return
            except ArgumentException:
                pass
        else:
            raise KeyError(
                "Couldn't find the LoadFile method in AssetsManager within C#"
            )

    def __init__(self) -> None:
        self._assetsmanager = AssetsManagerCS()

    def load_folder(self, folder: str):
        self._assetsmanager.LoadFolder(folder)

    def load_file(self, file: str):
        self._assetsmanager.LoadFiles([file])

    def load_files(self, files: Union[str, List[str]]) -> None:
        self._assetsmanager.LoadFiles(files)

    def load_from_memory(self, data: Union[str, bytes, bytearray], path: str) -> None:
        stream = MemoryStream()
        stream.Write(data, 0, len(data))
        stream.Seek(0, SeekOrigin.Begin)
        fileReader = FileReaderCS(path, stream)

        if fileReader.FileType == FileTypeCS.ResourceFile:
            self._assetsmanager.resourceFileReaders.Add(
                os.path.basename(path), fileReader
            )
        else:
            AssetsManager._load_file(self._assetsmanager, fileReader)

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

    def __getattr__(self, key: str) -> Any:
        return getattr(self._assetsmanager, key)
