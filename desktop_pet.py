import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QMenu

from desktop_pet.param_db import ParamDB
from desktop_pet.ui_pet_chat import PetChat
from desktop_pet.pet_theme import PetTheme
from desktop_pet.ui_setting import UISetting


class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.index = 0

        # 初始化设置数据库
        self.setting = ParamDB()

        self.menu = None
        self.theme_main_count = 0
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
        self.ui_chat = PetChat(self.setting)

        # setting
        self.ui_setting = UISetting(self.setting)

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
        self.load_theme_main(count=0)

    def load_theme_main(self, count):
        main_ui_image = self.theme.load_pixmap(image_type="main_"+str(count), size=[self.width, self.height])
        if main_ui_image is not None:
            # print("main ui setPixmap")
            self.main_ui.setPixmap(main_ui_image)
            return True
        else:
            main_ui_image = self.theme.load_movie(image_type="main_"+str(count), size=[self.width, self.height])
            if main_ui_image is not None:
                # print("main ui setMovie")
                self.main_ui.setMovie(main_ui_image)
                return True
            else:
                # print("main_ui not found")
                return False

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
        menu_qss = '''
        QMenu {
            border: 1px solid #d6ecf0; /* 边框宽度为1px，颜色为#CCCCCC */
            border-radius: 15px; /* 边框圆角 */
            background-color: #e3f9fd; /* 背景颜色 */
            padding: 5px 5px 5px 5px; /* 菜单项距菜单顶部边界和底部边界分别有5px */
        }
        
        QMenu::item { /* 菜单子控件item，为菜单项在default的状态 */
            border: 0px solid transparent;
            border-radius: 2px; /* 边框圆角 */
            background-color: transparent;
            color: black; /* 文本颜色 */
            min-height: 30px; /* 菜单项的最小高度 */
            margin: 2px 5px 2px 10px; /* 菜单项距其上下菜单项分别有2px，距菜单左右边界分别有10px和5px */
            padding: 2px 2px 2px 2px; /* 也可使用padding定义菜单项与上下左右的距离 */
        }
        
        QMenu::item:selected { /* 为菜单项在selected的状态 */
            background-color: #e9f1f6;
        }

        QMenu::separator { /* 菜单子控件separator，定义菜单项之间的分隔线 */
            height: 1px;
            background: #CCCCCC;
            margin-left: 2px; /* 距离菜单左边界2px */
            margin-right: 2px; /* 距离菜单右边界2px */
        }
        '''
        self.menu = QMenu()
        self.menu.setStyleSheet(menu_qss)
        # print(self.mapToGlobal(pos))

        # open ai 聊天
        chat_option = self.menu.addAction('聊天')
        chat_option.triggered.connect(self.show_chat)

        theme_option = self.menu.addAction('换肤')
        theme_option.triggered.connect(self.rand_main)

        # open ai 设置
        setting_option = self.menu.addAction('设置')
        setting_option.triggered.connect(self.show_setting)

        # 退出
        exit_option = self.menu.addAction('退出')
        exit_option.triggered.connect(lambda: exit())

        self.menu.exec(self.mapToGlobal(pos))

    def show_chat(self):
        # print(self.pos())
        # print(self.mapToGlobal(QPoint(self.geometry().x(), self.geometry().y())))
        self.ui_chat.start_show(self)

    def show_setting(self):
        # print(self.pos())
        # print(self.mapToGlobal(QPoint(self.geometry().x(), self.geometry().y())))
        self.ui_setting.start_show(self)

    def rand_main(self):
        self.theme_main_count += 1
        status = self.load_theme_main(self.theme_main_count)
        if not status:
            self.theme_main_count = 0
            status = self.load_theme_main(self.theme_main_count)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
