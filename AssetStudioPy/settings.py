from ._load import load_assetstudio

load_assetstudio()

from AssetStudio import ImageFormat


class Settings:
    displayAll = False
    enablePreview = True
    displayInfo = True
    openAfterExport = True
    assetGroupOption = 0
    convertTexture = True
    convertAudio = True
    convertType = ImageFormat.Png
    eulerFilter = True
    filterPrecision = 0.25
    exportAllNodes = True
    exportSkins = True
    exportAnimations = True
    boneSize = 10
    fbxVersion = 3
    fbxFormat = 0
    scaleFactor = 1
    exportBlendShape = True
    castToBone = False
    restoreExtensionName = True
    exportAllUvsAsDiffuseMaps = False
