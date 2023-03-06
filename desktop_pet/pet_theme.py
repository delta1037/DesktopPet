import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

from desktop_pet.param_db import ParamDB


class PetTheme:
    def __init__(self, setting: ParamDB):
        self.setting = setting
        self.theme_root = "theme/" + self.setting.setting_get("theme_name") + "/"

    def load_pixmap(self, image_type="main", size=None):
        image_path = ""
        if image_type == "main":
            image_path = self.theme_root + 'main.png'
        elif image_type == "icon_chat_me":
            image_path = self.theme_root + 'chat_me.ico'
        elif image_type == "icon_chat_ai":
            image_path = self.theme_root + 'chat_ai.ico'
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            pixmap = None
            print("path is error, ", image_path)
        if size is not None and pixmap is not None:
            pixmap = pixmap.scaled(size[0], size[1], Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)
        return pixmap

    def load_icon(self, icon_type: str):
        print("load icon type, ", icon_type)
        return QIcon(self.load_pixmap(image_type="icon_" + icon_type))
