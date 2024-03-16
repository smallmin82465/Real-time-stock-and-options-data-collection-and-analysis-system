from distutils.core import setup
import py2exe

setup(
    console=[{'script': 'mainUI.py'}],  # 改為console而不是windows
    options={
        'py2exe': {
            'includes': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
            'packages': ['translations'],
            'bundle_files': 1,
            'compressed': True
        }
    },
    data_files=[('translations', ['translations/app_zh.qm', 'translations/app_en_US.qm'])]
)