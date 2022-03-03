fp = r"S:\Datamines\Phantom of the Kill\data\cache\Units\100111\3D\duel\prefab"

import os
import AssetStudioPy

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
SAMPLES = os.path.join(LOCAL_PATH, "tests", "samples")
EXTRACTED = os.path.join(LOCAL_PATH, "tests", "extracted")

am = AssetStudioPy.AssetsManager()
am.load_file(fp)
#am._read_assets()
am.process_assets()
for obj in am.get_objects():
    if obj.typeName == "Animator":
        ani = obj.toClassType()

        AssetStudioPy.ExportAnimator(ani, "D:\\test")