import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QMenu

from desktop_pet.param_db import ParamDB
from desktop_pet.ui_pet_chat import PetChat
from desktop_pet.pet_theme import PetTheme


class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.index = 0

        # 初始化设置数据库
        self.setting = ParamDB()

        self.menu = None
        self.main_ui = None
        self.theme = PetTheme(self.setting)

        # 一些暂定参数
        self.width = int(self.setting.setting_get("main_win_width"))
        self.height = int(self.setting.setting_get("main_win_height"))

        # 一些暂存变量
        self.drag_s_pos = None

        # 初始化UI
        self.init_ui()

        # chat
        self.pet_chat = PetChat(self.setting)

        self.show()

    def init_ui(self):
        # 设置窗口无边框，窗口始终处于顶层位置，窗口无按钮
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            # | Qt.WindowType.SubWindow
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
        self.main_ui.setPixmap(self.theme.load_pixmap(size=[self.width, self.height]))

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
        chat_option.triggered.connect(self.show_chat)

        # 退出
        exit_option = self.menu.addAction('退出')
        exit_option.triggered.connect(lambda: exit())

        self.menu.exec(self.mapToGlobal(pos))

    def show_chat(self):
        self.pet_chat.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
