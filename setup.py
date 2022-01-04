import setuptools
from AssetStudioPy import __version__ as version

# download AssetStudioCross
# so that its files will be registered as belonging to the module
# which is important for a clean uninstall
import os
import shutil
from AssetStudioPy.update import update_assetstudio
fp = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "AssetStudioPy",
    "AssetStudioUtility"
)
if os.path.exists(fp):
    shutil.rmtree(fp)
os.makedirs(fp)
update_assetstudio(fp = fp)

# parse README
with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="AssetStudioPy",
	packages=setuptools.find_packages(),
	include_package_data = True,
	version=version,
	author="K0lb3",
	description="A pythonnet wrapper around AssetStudio",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/K0lb3/AssetStudioPy",
	download_url="https://github.com/K0lb3/AssetStudioPy/tarball/master",
	keywords=['python', 'unity', 'unity-asset', 'python3', 'data-minig', 'unitypack', 'assetstudio', 'unity-asset-extractor'],
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
        'pythonnet @ https://github.com/pythonnet/pythonnet.git'
	]
)
