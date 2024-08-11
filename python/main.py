from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore, QtWidgets

from texture_retarget import TextureRetarget
from model import TextureModel
from view import TextureRetargeterUI

import sys


DEFAULT_RELOAD_PACKAGES = []

def maya_main_window():
    """ Hooks into maya to allow a PySide window to open as a child of maya

    :return:
    """
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=maya_main_window()):
        super().__init__()
        self.texture_retarget = TextureRetarget()
        self.setWindowTitle("Texture Retarget")

        self.setMinimumWidth(800)

        self.data = self.texture_retarget.files_to_retarget
        data_list = [[key, value] for key, value in self.data.items()]
        # Set up the model
        model = TextureModel(data_list)

        # Set up the MVC view/controller
        texture_retarget = TextureRetargeterUI(model, self.texture_retarget)
        texture_retarget.show()

        self.setCentralWidget(texture_retarget)


def unload_packages(silent=True, packages=None):
    if packages is None:
        packages = DEFAULT_RELOAD_PACKAGES

    # construct reload list
    reloadList = []
    for i in sys.modules.keys():
        for package in packages:
            if i.startswith(package):
                reloadList.append(i)

    # unload everything
    for i in reloadList:
        try:
            if sys.modules[i] is not None:
                del(sys.modules[i])
                if not silent:
                    print("Unloaded: %s" % i)
        except:
            print("Failed to unload: %s" % i)


unload_packages(silent=False, packages=["model", "view", "texture_retarget"])

window = MainWindow()
window.show()
