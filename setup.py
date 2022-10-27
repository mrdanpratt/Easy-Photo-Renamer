from setuptools import setup

APP = ['EasyPhotoRenamer.py']
DATA_FILES = ['EasyPhotoRenamerLogo.png', 'NoFurtherPhotos.png', 'NoPreviousPhotos.png', 'PicRenamerDefaultPic.png', 'PicRenamerPhotoNotFound.png']
OPTIONS = {
    'iconfile': 'EasyPhotoRenamerLogo.icns',
    'plist': {
        'CFBundleName': 'Easy Photo Renamer',
        'CFBundleShortVersionString': '0.1',
        'CFBundleVersion': '0.1.0',
        'NSHumanReadableCopyright': 'Copyright © 2022 Dan Pratt\n\nThis software is distributed under the terms\nof the MIT License.',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)