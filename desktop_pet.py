import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QMenu

from desktop_pet.pet_image_ctrl import PetImage


class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.index = 0

        self.menu = None
        self.main_ui = None
        self.image_ctrl = PetImage()

        # 一些暂定参数
        self.width = 128
        self.height = 128

        # 一些暂存变量
        self.drag_s_pos = None

        # 初始化UI
        self.init_ui()
        self.show()

    def init_ui(self):
        # 设置窗口无边框，窗口始终处于顶层位置，窗口无按钮
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.SubWindow
        )
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.repaint()
        self.resize(self.width, self.height)

        # 右键响应
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContexMenu)

        # 主窗口UI图像
        self.main_ui = QLabel(self)
        self.main_ui.setPixmap(self.image_ctrl.load_pixmap(size=[self.width, self.height]))

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        # print(e.type().DragEnter)
        if a0.button() == Qt.MouseButton.LeftButton:
            # 将拖动绑定到左键
            self.drag_s_pos = a0.pos()
        # if a0.button() == Qt.MouseButton.RightButton:
        #     print("right")

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.drag_s_pos is None:
            return
        # 拖动界面
        move_cor = a0.pos() - self.drag_s_pos
        self.move(self.mapToParent(move_cor))

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.drag_s_pos = None

    def showContexMenu(self, pos: QPoint):
        self.menu = QMenu()

        # open ai 聊天
        chat_option = self.menu.addAction('聊天')
        chat_option.triggered.connect(lambda: exit())

        # 退出
        exit_option = self.menu.addAction('退出')
        exit_option.triggered.connect(lambda: exit())

        self.menu.exec(self.mapToGlobal(pos))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
