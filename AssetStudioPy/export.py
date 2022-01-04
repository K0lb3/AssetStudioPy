from typing import Union
from ._load import load_assetstudio

load_assetstudio()
from .settings import Settings

# port sealed AssetStudioGUI.Exporter and make it pythonic
from System.IO import File
from AssetStudio import (
    ModelConverter,
    ModelExporter,
    ObjectReader,
    Animator,
    GameObject,
    Texture2D,
    Texture2DExtensions,
    ImageExtensions,
    ImageFormat,
    AudioClip,
    Shader,
    TextAsset,
    Mesh,
    Material,
    Font,
    MonoBehaviour,
    AnimationClip,
    AudioClipConverter,
    VideoClip,
    MovieTexture,
    Sprite,
)

# TODO - add extention to paths and some other stuff

from PIL import Image


def ExportTexture2D(
    m_Texture2D: Texture2D,
    exportPath: str = None,
    convert_texture: bool = True,
    extension=".png",
) -> Union[bytearray, None]:
    """[summary]

    Args:
        m_Texture2D (Texture2D): [Texture2D to be exported]
        exportPath (str): [Saves the texture to this path. If no path is given, the texture won't be saved and only the image will be returned.]
        convert_texture (bool, optional): [Convert the texture to an image or keep it as texture]. Defaults to True.

    Returns:
        [Image, bytearray]: [converted texture]
    """
    if convert_texture:
        image = Texture2DExtensions.ConvertToImage(m_Texture2D, True)
        if not image:
            return None
        if exportPath:
            fs = File.OpenWrite(exportPath)
            # TODO - decide based on extension
            ImageExtensions.WriteToStream(image, fs, ImageFormat.Png)
            fs.Close()
        ret = Image.frombuffer(
            "RGBA",
            (image.Width, image.Height),
            bytes(ImageExtensions.ConvertToBgra32Bytes(image)),
            "raw",
            "BGRA",
        )
    else:
        ret = bytearray(m_Texture2D.image_data.GetData())
        if exportPath:
            with open(exportPath, "wb") as f:
                f.write(ret)
    return ret


def ExportAudioClip(
    m_AudioClip: AudioClip, exportPath: str = None
) -> Union[bytearray, None]:
    """[summary]

    Args:
        m_AudioClip (AudioClip): [AudioClip to be exported]
        exportPath (str, optional): [Saves the audio to this path. If no path is given, the audio won't be saved and only the audio will be returned.]

    Returns:
        [bytearray]: [converted audio]
    """
    m_AudioData = m_AudioClip.m_AudioData.GetData()
    if not m_AudioData or m_AudioData.Length == 0:
        return None
    converter = AudioClipConverter(m_AudioClip)
    if converter.IsSupport:
        buffer = bytearray(converter.ConvertToWav())
        if not buffer:
            return None
        if exportPath:
            # TODO - might have to append wav
            with open(exportPath, "wb") as f:
                f.write(buffer)
        ret = buffer
    else:
        # TODO, add converter.GetExtensionName() to filename
        ret = bytearray(m_AudioData)
        if exportPath:
            with open(exportPath, "wb") as f:
                f.write(ret)
    return ret


def ExportShader(m_Shader: Shader, exportPath: str, extension=".shader") -> str:
    """[summary]

    Args:
        m_Shader (Shader): [Shader to be exported]
        exportPath (str): [Saves the shader to this path. If no path is given, the shader won't be saved and only the shader will be returned.]

    Returns:
        [bytearray]: [converted shader]
    """
    shader = m_Shader.Convert()
    if exportPath:
        with open(exportPath, "wt", encoding="utf8") as f:
            f.write(shader)
    return shader


def ExportTextAsset(
    m_TextAsset: TextAsset, exportPath: str, extension=".txt"
) -> bytearray:
    # if (Settings.restoreExtensionName)
    # {
    #     if (!string.IsNullOrEmpty(item.Container))
    #     {
    #         extension = Path.GetExtension(item.Container);
    #     }
    # }
    ret = bytearray(m_TextAsset.m_Script)
    if exportPath:
        with open(exportPath, "wb") as f:
            f.write(ret)
    return ret


def ExportMonoBehaviour(
    m_MonoBehaviour: MonoBehaviour, exportPath: str, extension: str = ".json"
) -> Union[str, bytearray]:
    type = m_MonoBehaviour.ToType()
    if type:
        # TODO - situated in GUI that we want to ditch
        # m_Type = Studio.MonoBehaviourToTypeTree(m_MonoBehaviour)
        # type = m_MonoBehaviour.ToType(m_Type)
        pass
    input("check this via debugger")
    # ret = JsonConvert.SerializeObject(type, Formatting.Indented)
    # File.WriteAllText(exportFullPath, str);
    # return true;


def ExportFont(
    m_Font: Font, exportPath: str, extenions: str = ".ttf"
) -> Union[bytearray, None]:
    """[summary]

    Args:
        m_Font (Font): [Font to be exported]
        exportPath (str): [Saves the font to this path. If no path is given, the font won't be saved and only the font will be returned.]

    Returns:
        [bytearray]: [converted font]
    """
    if m_Font.m_FontData:
        fontdata = bytearray(m_Font.m_FontData)
        extension = ".ttf"
        if fontdata.startswith(b"OTTO"):
            extension = ".otf"

        if exportPath:
            with open(exportPath, "wb") as f:
                f.write(fontdata)
        return fontdata


# def ExportMesh(AssetItem item, string exportPath)
# {
#     var m_Mesh = (Mesh)item.Asset;
#     if (m_Mesh.m_VertexCount <= 0)
#         return false;
#     if (!TryExportFile(exportPath, item, ".obj", out var exportFullPath))
#         return false;
#     var sb = new StringBuilder();
#     sb.AppendLine("g " + m_Mesh.m_Name);
#     #region Vertices
#     if (m_Mesh.m_Vertices == null || m_Mesh.m_Vertices.Length == 0)
#     {
#         return false;
#     }
#     int c = 3;
#     if (m_Mesh.m_Vertices.Length == m_Mesh.m_VertexCount * 4)
#     {
#         c = 4;
#     }
#     for (int v = 0; v < m_Mesh.m_VertexCount; v++)
#     {
#         sb.AppendFormat("v {0} {1} {2}\r\n", -m_Mesh.m_Vertices[v * c], m_Mesh.m_Vertices[v * c + 1], m_Mesh.m_Vertices[v * c + 2]);
#     }
#     #endregion

#     #region UV
#     if (m_Mesh.m_UV0?.Length > 0)
#     {
#         if (m_Mesh.m_UV0.Length == m_Mesh.m_VertexCount * 2)
#         {
#             c = 2;
#         }
#         else if (m_Mesh.m_UV0.Length == m_Mesh.m_VertexCount * 3)
#         {
#             c = 3;
#         }
#         for (int v = 0; v < m_Mesh.m_VertexCount; v++)
#         {
#             sb.AppendFormat("vt {0} {1}\r\n", m_Mesh.m_UV0[v * c], m_Mesh.m_UV0[v * c + 1]);
#         }
#     }
#     #endregion

#     #region Normals
#     if (m_Mesh.m_Normals?.Length > 0)
#     {
#         if (m_Mesh.m_Normals.Length == m_Mesh.m_VertexCount * 3)
#         {
#             c = 3;
#         }
#         else if (m_Mesh.m_Normals.Length == m_Mesh.m_VertexCount * 4)
#         {
#             c = 4;
#         }
#         for (int v = 0; v < m_Mesh.m_VertexCount; v++)
#         {
#             sb.AppendFormat("vn {0} {1} {2}\r\n", -m_Mesh.m_Normals[v * c], m_Mesh.m_Normals[v * c + 1], m_Mesh.m_Normals[v * c + 2]);
#         }
#     }
#     #endregion

#     #region Face
#     int sum = 0;
#     for (var i = 0; i < m_Mesh.m_SubMeshes.Length; i++)
#     {
#         sb.AppendLine($"g {m_Mesh.m_Name}_{i}");
#         int indexCount = (int)m_Mesh.m_SubMeshes[i].indexCount;
#         var end = sum + indexCount / 3;
#         for (int f = sum; f < end; f++)
#         {
#             sb.AppendFormat("f {0}/{0}/{0} {1}/{1}/{1} {2}/{2}/{2}\r\n", m_Mesh.m_Indices[f * 3 + 2] + 1, m_Mesh.m_Indices[f * 3 + 1] + 1, m_Mesh.m_Indices[f * 3] + 1);
#         }
#         sum = end;
#     }
#     #endregion

#     sb.Replace("NaN", "0");
#     File.WriteAllText(exportFullPath, sb.ToString());
#     return true;
# }


def ExportVideoClip(m_VideoClip: VideoClip, exportPath: str) -> Union[bytearray, None]:
    if m_VideoClip.m_ExternalResources.m_Size > 0:
        # TODO - Path.GetExtension(m_VideoClip.m_OriginalPath)
        if exportPath:
            m_VideoClip.m_VideoData.WriteData(exportPath)
        return bytearray(m_VideoClip.m_VideoData.GetData())


def ExportMovieTexture(
    m_MovieTexture: MovieTexture, exportPath: str, extension: str = ".ogv"
) -> Union[bytearray, None]:
    ret = bytearray(m_MovieTexture.m_MovieData)
    if exportPath:
        with open(exportPath, "wb") as f:
            f.write(ret)
    return ret


def ExportSprite(m_Sprite: Sprite, exportPath: str):
    # TODO - AssetStudio ignored the alpha channel
    image = m_Sprite.GetImage()


# def ExportRawFile(obj: ObjectReader, exportPath: str, extension: str = ".dat") -> bytearray:
#     ret = bytearray(obj.GetRawData())
# {
#     if (!TryExportFile(exportPath, item, ".dat", out var exportFullPath))
#         return false;
#     File.WriteAllBytes(exportFullPath, item.Asset.GetRawData());
#     return true;
# }


def ExportAnimator(
    m_Animator: Animator,
    exportPath: str,
    animationList: list = None,
    extension: str = ".fbx",
):
    #     var exportFullPath = Path.Combine(exportPath, item.Text, item.Text + ".fbx");
    #     if (File.Exists(exportFullPath))
    #     {
    #         exportFullPath = Path.Combine(exportPath, item.Text + item.UniqueID, item.Text + ".fbx");
    #     }
    convert = (
        ModelConverter(m_Animator, Settings.convertType, animationList)
        if animationList
        else ModelConverter(m_Animator, Settings.convertType)
    )
    ExportFbx(convert, exportPath)


def ExportGameObject(
    gameObject: GameObject,
    exportPath: str,
    animationList: list = None,
    extension: str = ".fbx",
):
    convert = (
        ModelConverter(gameObject, Settings.convertType, animationList)
        if animationList
        else ModelConverter(gameObject, Settings.convertType)
    )
    # exportPath = exportPath + FixFileName(gameObject.m_Name) + ".fbx";
    ExportFbx(convert, exportPath)


# public static void ExportGameObjectMerge(List<GameObject> gameObject, string exportPath, List<AssetItem> animationList = null)
# {
#     var rootName = Path.GetFileNameWithoutExtension(exportPath);
#     var convert = animationList != null
#         ? new ModelConverter(rootName, gameObject, Settings.convertType, animationList.Select(x => (AnimationClip)x.Asset).ToArray())
#         : new ModelConverter(rootName, gameObject, Settings.convertType);
#     ExportFbx(convert, exportPath);
# }


def ExportFbx(convert, exportPath: str):
    eulerFilter = Settings.eulerFilter
    filterPrecision = float(Settings.filterPrecision)
    exportAllNodes = Settings.exportAllNodes
    exportSkins = Settings.exportSkins
    exportAnimations = Settings.exportAnimations
    exportBlendShape = Settings.exportBlendShape
    castToBone = Settings.castToBone
    boneSize = int(Settings.boneSize)
    exportAllUvsAsDiffuseMaps = Settings.exportAllUvsAsDiffuseMaps
    scaleFactor = float(Settings.scaleFactor)
    fbxVersion = Settings.fbxVersion
    fbxFormat = Settings.fbxFormat
    ModelExporter.ExportFbx(
        exportPath,
        convert,
        eulerFilter,
        filterPrecision,
        exportAllNodes,
        exportSkins,
        exportAnimations,
        exportBlendShape,
        castToBone,
        boneSize,
        exportAllUvsAsDiffuseMaps,
        scaleFactor,
        fbxVersion,
        fbxFormat == 1,
    )


# def ExportDumpFile(AssetItem item, string exportPath)
# {
#     if (!TryExportFile(exportPath, item, ".txt", out var exportFullPath))
#         return false;
#     var str = item.Asset.Dump();
#     if (str == null && item.Asset is MonoBehaviour m_MonoBehaviour)
#     {
#         var m_Type = Studio.MonoBehaviourToTypeTree(m_MonoBehaviour);
#         str = m_MonoBehaviour.Dump(m_Type);
#     }
#     if (str != null)
#     {
#         File.WriteAllText(exportFullPath, str);
#         return true;
#     }
#     return false;
# }

# def ExportConvertFile(AssetItem item, string exportPath)
# {
#     switch (item.Type)
#     {
#         case ClassIDType.Texture2D:
#             return ExportTexture2D(item, exportPath);
#         case ClassIDType.AudioClip:
#             return ExportAudioClip(item, exportPath);
#         case ClassIDType.Shader:
#             return ExportShader(item, exportPath);
#         case ClassIDType.TextAsset:
#             return ExportTextAsset(item, exportPath);
#         case ClassIDType.MonoBehaviour:
#             return ExportMonoBehaviour(item, exportPath);
#         case ClassIDType.Font:
#             return ExportFont(item, exportPath);
#         case ClassIDType.Mesh:
#             return ExportMesh(item, exportPath);
#         case ClassIDType.VideoClip:
#             return ExportVideoClip(item, exportPath);
#         case ClassIDType.MovieTexture:
#             return ExportMovieTexture(item, exportPath);
#         case ClassIDType.Sprite:
#             return ExportSprite(item, exportPath);
#         case ClassIDType.Animator:
#             return ExportAnimator(item, exportPath);
#         case ClassIDType.AnimationClip:
#             return false;
#         default:
#             return ExportRawFile(item, exportPath);
#     }
# }

import re
from System.IO import Path

reInvalidFileNameChars = re.compile(f"[{''.join(Path.GetInvalidFileNameChars())}]")


def FixFileName(name: str) -> str:
    if len(name) >= 260:
        # TODO: REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
        return Path.GetRandomFileName()

    return reInvalidFileNameChars.sub("_", name)
