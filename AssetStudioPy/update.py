from urllib.request import urlopen
import json
import platform
from zipfile import ZipFile
from io import BytesIO
import os

def detect_platform():
    # Linux, Windows, Darwin
    system = platform.system()
    if system == "Darwin":
        system = "macOS"
    # 32bit, 64bit,
    arch = platform.architecture()[0]
    if arch == "32bit":
        arch = "x86"
    elif arch == "64bit":
        arch = "x64"
    else:
        raise NotImplemented(
            f"Architecture ({arch}) is not supported, please report this issue on GitHub"
        )
    # for arm detection
    machine = platform.machine()
    if "arm" in machine:
        if arch == "32bit":
            raise NotImplemented(
                f"Architecture ({arch}) is not supported, please report this issue on GitHub"
            )
        elif arch == "64bit":
            arch = "arm64"
    return system, arch


def update_assetstudio(
    net="net6.0",
    release_url="https://api.github.com/repos/K0lb3/AssetStudio/releases/latest",
    fp=None,
):
    """Update AssetStudio (Cross Platform version) to the latest version.

    Args:
        net (str, optional): net version, net5.0 or net6.0. Defaults to "net6.0".
        build (str, optional): build type, so far only Release exists. Defaults to "Release".
        release_url (str, optional): api link to the release source. Defaults to "https://api.github.com/repos/K0lb3/AssetStudio/releases/latest".
        fp ([type], optional): filepath where the update shall be installed to. If none is set, the AssetStudioPy one will be updated.

    Raises:
        FileNotFoundError: [description]
    """
    if not fp:
        fp = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "AssetStudioUtility"
        )
    system, arch = detect_platform()
    name = f"AssetStudioUtility.{net}.{system}.{arch}.zip"
    release = json.loads(urlopen(release_url).read())
    for asset in release.get("assets", []):
        if asset.get("name") == name:
            print(f"Downloading {name}")
            url = asset.get("browser_download_url")
            zip_raw = urlopen(url).read()
            with BytesIO(zip_raw) as zip_stream:
                print(f"Extracting {name}")
                with ZipFile(zip_stream) as zip:
                    zip.extractall(fp)
            print("AssetStudioUtility updated!")
            return
    else:
        raise FileNotFoundError(f"No build found for this system ({name})")


if __name__ == "__main__":
    update_assetstudio()
