from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class PetImage:
    def __init__(self):
        self.image_root = "resource/"

    def load_pixmap(self, image_type="main", size=None):
        pixmap = QPixmap(self.image_root + 'shime1.png')
        if size is not None:
            pixmap = pixmap.scaled(size[0], size[1], Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)
        return pixmap
