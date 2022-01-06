import setuptools
import importlib.util

# download AssetStudioCross
# so that its files will be registered as belonging to the module
# which is important for a clean uninstall
import os

local_fp = os.path.dirname(os.path.realpath(__file__))
assetstudiopy_fp = os.path.join(local_fp, "AssetStudioPy")
assetstudiopyutility_fp = os.path.join(assetstudiopy_fp, "AssetStudioUtility")


def manual_module_import(modulename):
    """Manually import a module to bypass the Utility loading via __init__"""
    spec = importlib.util.spec_from_file_location(
        "AssetStudioPy.update", os.path.join(assetstudiopy_fp, f"{modulename}.py")
    )
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


if not os.path.exists(assetstudiopyutility_fp):
    print("No local AssetStudioUtility found, downloading the latest release")
    update = manual_module_import("update")
    update.update_assetstudio(fp=assetstudiopyutility_fp)

# import version, author and description
version = manual_module_import("_version")

# parse README
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AssetStudioPy",
    packages=setuptools.find_packages(),
    include_package_data=True,
    version=version.__version__,
    author=version.__author__,
    description=version.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/K0lb3/AssetStudioPy",
    download_url="https://github.com/K0lb3/AssetStudioPy/tarball/master",
    keywords=[
        "python",
        "unity",
        "unity-asset",
        "python3",
        "data-minig",
        "unitypack",
        "assetstudio",
        "unity-asset-extractor",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
    ],
    install_requires=[
        "Pillow",
        "pythonnet @ git+https://github.com/pythonnet/pythonnet.git"
    ],
)

# check if dotnet is installed
# if not, print a warning
sdks = os.popen("dotnet --list-sdks").read()
runtimes = os.popen("dotnet --list-runtimes").read()
if not ("6.0." in sdks or "6.0." in runtimes):
    print(
        """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Couldn't detect a local .net 6.0 installation.
AssetStudioPy won't work besides if you use a custom setup.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
    )
