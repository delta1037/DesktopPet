import os.path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QMovie

from desktop_pet.param_db import ParamDB


class PetTheme:
    def __init__(self, setting: ParamDB):
        self.setting = setting
        self.theme_root = "theme/" + self.setting.setting_get("theme_name") + "/"

    def load_pixmap(self, image_type="main", size=None):
        image_path = ""
        if image_type.startswith("main"):
            image_path = self.theme_root + image_type + '.png'
        elif image_type == "icon_chat_me":
            image_path = self.theme_root + 'chat_me.ico'
        elif image_type == "icon_chat_ai":
            image_path = self.theme_root + 'chat_ai.ico'
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            print("load_pixmap path is error, ", image_path)
            return None

        if size is not None and pixmap is not None:
            pixmap = pixmap.scaled(size[0], size[1], Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)
        return pixmap

    def load_movie(self, image_type="main", size=None):
        image_path = ""
        if image_type.startswith("main"):
            image_path = self.theme_root + image_type + '.gif'
        if os.path.exists(image_path):
            movie = QMovie(image_path)
        else:
            print("load_movie path is error, ", image_path)
            return None
        if size is not None and movie is not None:
            movie.setCacheMode(QMovie.CacheMode.CacheAll)
            movie.setScaledSize(QSize(size[0], size[1]))
            movie.start()
        return movie

    def load_icon(self, icon_type: str):
        print("load icon type, ", icon_type)
        return QIcon(self.load_pixmap(image_type="icon_" + icon_type))
