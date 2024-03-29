import os
import AssetStudioPy

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
SAMPLES = os.path.join(LOCAL_PATH, "samples")
EXTRACTED = os.path.join(LOCAL_PATH, "extracted")

# utility
from PIL import Image
from tempfile import TemporaryDirectory


def calc_binary_dif(bin1: bytes, bin2: bytes) -> float:
    # use hash check
    if bin1 == bin2:
        return 0.0
    else:
        return sum(x != y for x, y in zip(bin1, bin2)) / (min(len(bin1), len(bin2)))


def test_loading_assets():
    print("Testing different load functions")
    am = AssetStudioPy.AssetsManager()

    def check_object_count():
        obj_count = len(list(am.get_objects()))
        print(am.assetsFileList.Count, obj_count)
        assert obj_count == 6684
        am.Clear()

    print("file via file path")
    for f in os.listdir(SAMPLES):
        am.load_file(os.path.join(SAMPLES, f))
    check_object_count()

    print("folder via file path")
    am = AssetStudioPy.AssetsManager()
    am.load_folder(SAMPLES)
    check_object_count()

    print("file via memory")
    for fn in os.listdir(SAMPLES):
        with open(os.path.join(SAMPLES, fn), "rb") as f:
            am.load_from_memory(f.read(), fn)
    check_object_count()


def test_animator():
    print("test Animator")
    fp = os.path.join(SAMPLES, "data")

    fname = "MaintenanceWindow.fbx"

    am = AssetStudioPy.AssetsManager()
    am.load_file(fp)
    for obj in am.get_objects():
        if obj.m_PathID == 441 and obj.typeName == "Animator":
            ani = obj.toClassType()
            with open(os.path.join(EXTRACTED, fname), "rb") as f:
                fbx = f.read()
            with TemporaryDirectory() as tempdir:
                fp = os.path.join(tempdir, fname)
                AssetStudioPy.ExportAnimator(ani, fp)
                with open(os.path.join(tempdir, fp), "rb") as f:
                    live_fbx = f.read()
            print(len(fbx))
            print(len(live_fbx))
            bin_dif = calc_binary_dif(fbx, live_fbx)
            print(bin_dif)
            assert len(fbx) == len(live_fbx)
            break
    else:
        raise LookupError("Couldn't find the Animator")


def test_audioclip():
    print("test AudioClip")
    fp = os.path.join(SAMPLES, "audioclip")

    expected_name = "CN_021"

    am = AssetStudioPy.AssetsManager()
    am.load_file(fp)
    for obj in am.get_objects():
        if obj.m_PathID == -4299652749329800113:
            ac = obj.toClassType()
            assert expected_name == ac.m_Name
            with open(os.path.join(EXTRACTED, f"{expected_name}.wav"), "rb") as f:
                audio = f.read()
            live_audio = AssetStudioPy.ExportAudioClip(ac)
            print(len(audio))
            print(len(live_audio))
            bin_dif = calc_binary_dif(audio, live_audio)
            print(bin_dif)
            assert len(audio) == len(live_audio)
            break
    else:
        raise LookupError("Couldn't find the AudioClip")


def test_textasset():
    print("test TextAsset")
    fp = os.path.join(SAMPLES, "textasset")

    expected_name = "PartTitle"
    expected_data = """{
    "infos": [
        {
            "key": "PA_ST_01",
            "value": "第１部"
        }
    ]
}""".encode(
        "utf8"
    )

    am = AssetStudioPy.AssetsManager()
    am.load_file(fp)
    for obj in am.get_objects():
        if obj.m_PathID == 412072573404675682:
            ta = obj.toClassType()
            assert expected_name == ta.m_Name
            assert expected_data == bytes(ta.m_Script)
            break
    else:
        raise LookupError("Couldn't find the TextAsset")


def test_texture2d():
    print("test Texture2D")
    fp = os.path.join(SAMPLES, "sprite")

    expected_name = "banner_1"

    am = AssetStudioPy.AssetsManager()
    am.load_file(fp)
    for obj in am.get_objects():
        if obj.m_PathID == -3875358842991402074:
            tex = obj.toClassType()
            assert expected_name == tex.m_Name
            img = Image.open(os.path.join(EXTRACTED, f"{expected_name}.png"))
            live_img = AssetStudioPy.ExportTexture2D(tex)
            assert img.tobytes() == live_img.tobytes()
            break
    else:
        raise LookupError("Couldn't find the Texture2D")


def test_sprite():
    print("test Sprite")
    fp = os.path.join(SAMPLES, "sprite")

    expected_name = "banner_1"

    am = AssetStudioPy.AssetsManager()
    am.load_file(fp)
    for obj in am.get_objects():
        if obj.m_PathID == -8325468307350463555:
            tex = obj.toClassType()
            assert expected_name == tex.m_Name
            img = Image.open(os.path.join(EXTRACTED, f"{expected_name}_sprite.png"))
            live_img = AssetStudioPy.ExportSprite(tex)
            assert img.tobytes() == live_img.tobytes()
            break
    else:
        raise LookupError("Couldn't find the Texture2D")


# def test_mesh():
#     env = UnityPy.load(os.path.join(SAMPLES, "xinzexi_2_n_tex"))
#     with open(os.path.join(SAMPLES, 'xinzexi_2_n_tex_mesh'), 'rb') as f:
#         wanted = f.read().replace(b'\r', b'')
#     for obj in env.objects:
#         if obj.type == "Mesh":
#             mesh = obj.read()
#             data = mesh.export()
#             if isinstance(data, str):
#                 data = data.encode('utf8').replace(b'\r', b'')
#             assert data == wanted


if __name__ == "__main__":
    for x in list(locals()):
        if str(x)[:4] == "test":
            try:
                locals()[x]()
            except AssertionError:
                print("assertion failed")
    input("All Tests Passed")
