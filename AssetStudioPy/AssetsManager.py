import os
from typing import Dict, Union, List, Tuple, Iterator, Any
from ._load import load_assetstudio, get_class_method, get_class_fields

load_assetstudio()

from .ObjectReader import ObjectReader
import AssetStudio
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
    _fields: Dict[str, "FieldInfo"] = {}

    @staticmethod
    def _load_file(assetsmanager: AssetsManagerCS, filereader: FileReaderCS):
        if not (
            isinstance(assetsmanager, AssetsManagerCS)
            and isinstance(filereader, FileReaderCS)
        ):
            raise ValueError("Invalid input types")

        for method in get_class_method(AssetsManagerCS, "LoadFile"):
            if method.GetParameters()[0].Name == "reader":
                method.Invoke(assetsmanager, [filereader])
                AssetsManager._load_file = (
                    lambda assetsmanager, filereader: method.Invoke(
                        assetsmanager, [filereader]
                    )
                )
                return
        else:
            raise KeyError(
                "Couldn't find the LoadFile method in AssetsManager within C#"
            )

    @staticmethod
    def _get_assetsmanager_private_function(key):
        return (
            method
            for method in get_class_method(AssetsManagerCS, key)
            if method.IsPrivate
        )

    def end_load(self) -> None:
        self.importFiles.Clear()
        # self.importFilesHash.Clear()
        self.assetsFileListHash.Clear()

        self.ReadAssets()
        self.ProcessAssets()

    def __init__(self) -> None:
        self._assetsmanager = AssetsManagerCS()
        self._fields = get_class_fields(AssetsManagerCS)

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

        # resourceFileReaders
        if fileReader.FileType == FileTypeCS.ResourceFile:
            self.resourceFileReaders.TryAdd(os.path.basename(path), fileReader)
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
        if key in self._fields:
            return self._fields[key].GetValue(self._assetsmanager)
        return getattr(self._assetsmanager, key)

    def read_assets(self):
        # reflection has some problems with it
        for assetsFile in self.assetsFileList:
            for objectInfo in assetsFile.m_Objects:
                objectReader = ObjectReaderCS(assetsFile.reader, assetsFile, objectInfo)
                try:
                    # Object obj
                    objType = objectReader.type
                    if objType == ClassIDTypeCS.Animation:
                        obj = AssetStudio.Animation(objectReader)
                    elif objType == ClassIDTypeCS.AnimationClip:
                        obj = AssetStudio.AnimationClip(objectReader)
                    elif objType == ClassIDTypeCS.Animator:
                        obj = AssetStudio.Animator(objectReader)
                    elif objType == ClassIDTypeCS.AnimatorController:
                        obj = AssetStudio.AnimatorController(objectReader)
                    elif objType == ClassIDTypeCS.AnimatorOverrideController:
                        obj = AssetStudio.AnimatorOverrideController(objectReader)
                    elif objType == ClassIDTypeCS.AssetBundle:
                        obj = AssetStudio.AssetBundle(objectReader)
                    elif objType == ClassIDTypeCS.AudioClip:
                        obj = AssetStudio.AudioClip(objectReader)
                    elif objType == ClassIDTypeCS.Avatar:
                        obj = AssetStudio.Avatar(objectReader)
                    elif objType == ClassIDTypeCS.Font:
                        obj = AssetStudio.Font(objectReader)
                    elif objType == ClassIDTypeCS.GameObject:
                        obj = AssetStudio.GameObject(objectReader)
                    elif objType == ClassIDTypeCS.Material:
                        obj = AssetStudio.Material(objectReader)
                    elif objType == ClassIDTypeCS.Mesh:
                        obj = AssetStudio.Mesh(objectReader)
                    elif objType == ClassIDTypeCS.MeshFilter:
                        obj = AssetStudio.MeshFilter(objectReader)
                    elif objType == ClassIDTypeCS.MeshRenderer:
                        obj = AssetStudio.MeshRenderer(objectReader)
                    elif objType == ClassIDTypeCS.MonoBehaviour:
                        obj = AssetStudio.MonoBehaviour(objectReader)
                    elif objType == ClassIDTypeCS.MonoScript:
                        obj = AssetStudio.MonoScript(objectReader)
                    elif objType == ClassIDTypeCS.MovieTexture:
                        obj = AssetStudio.MovieTexture(objectReader)
                    elif objType == ClassIDTypeCS.PlayerSettings:
                        obj = AssetStudio.PlayerSettings(objectReader)
                    elif objType == ClassIDTypeCS.RectTransform:
                        obj = AssetStudio.RectTransform(objectReader)
                    elif objType == ClassIDTypeCS.Shader:
                        obj = AssetStudio.Shader(objectReader)
                    elif objType == ClassIDTypeCS.SkinnedMeshRenderer:
                        obj = AssetStudio.SkinnedMeshRenderer(objectReader)
                    elif objType == ClassIDTypeCS.Sprite:
                        obj = AssetStudio.Sprite(objectReader)
                    elif objType == ClassIDTypeCS.SpriteAtlas:
                        obj = AssetStudio.SpriteAtlas(objectReader)
                    elif objType == ClassIDTypeCS.TextAsset:
                        obj = AssetStudio.TextAsset(objectReader)
                    elif objType == ClassIDTypeCS.Texture2D:
                        obj = AssetStudio.Texture2D(objectReader)
                    elif objType == ClassIDTypeCS.Transform:
                        obj = AssetStudio.Transform(objectReader)
                    elif objType == ClassIDTypeCS.VideoClip:
                        obj = AssetStudio.VideoClip(objectReader)
                    elif objType == ClassIDTypeCS.ResourceManager:
                        obj = AssetStudio.ResourceManager(objectReader)
                    else:
                        obj = AssetStudio.Object(objectReader)

                    assetsFile.AddObject(obj)
                except Exception as e:
                    sb = [
                        "Unable to load object",
                        f"Assets {assetsFile.fileName}",
                        f"Path {assetsFile.originalPath}",
                        f"Type {objectReader.type}",
                        f"PathID {objectInfo.m_PathID}",
                        str(e),
                    ]
                    # Logger.Error(sb.ToString())

    def process_assets(self):
        for assetsFile in self.assetsFileList:
            for obj in assetsFile.Objects:
                if obj.type == ClassIDTypeCS.GameObject:
                    for pptr in obj.m_Components:
                        res, m_Component = pptr.TryGet()
                        if res:
                            if m_Component.type == ClassIDTypeCS.Transform:
                                obj.m_Transform = m_Component
                            elif m_Component.type == ClassIDTypeCS.MeshRenderer:
                                obj.m_MeshRenderer = m_Component
                            elif m_Component.type == ClassIDTypeCS.MeshFilter:
                                obj.m_MeshFilter = m_Component
                            elif m_Component.type == ClassIDTypeCS.SkinnedMeshRenderer:
                                obj.m_SkinnedMeshRenderer = m_Component
                            elif m_Component.type == ClassIDTypeCS.Animator:
                                obj.m_Animator = m_Component
                            elif m_Component.type == ClassIDTypeCS.Animation:
                                obj.m_Animation = m_Component

                elif obj.type == ClassIDTypeCS.SpriteAtlas:
                    if obj.m_IsVariant:
                        continue

                    for m_PackedSprite in obj.m_PackedSprites:
                        res, m_Sprite = m_PackedSprite.TryGet()
                        if res and m_Sprite.m_SpriteAtlas.IsNull:
                            m_Sprite.m_SpriteAtlas.Set(obj)
