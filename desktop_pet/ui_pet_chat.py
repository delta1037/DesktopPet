import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QGuiApplication, QScreen
from PyQt6.QtWidgets import *

from desktop_pet.chat_openai import OpenAIChat
from desktop_pet.param_db import ParamDB
from desktop_pet.pet_theme import PetTheme


class PetChat(QWidget):
    def __init__(self, setting: ParamDB, parent=None, **kwargs):
        super(PetChat, self).__init__(parent)
        self.setting = setting

        self.ai_prefix = self.setting.setting_get("chat_ai_prefix")
        self.me_suffix = self.setting.setting_get("chat_me_prefix")

        self.chat_win_width = int(self.setting.setting_get("chat_win_width"))
        self.chat_win_height = int(self.setting.setting_get("chat_win_height"))
        self.resize(self.chat_win_width, self.chat_win_height)
        self.theme = PetTheme(self.setting)

        # 对话模型
        self.chat_messages = [{
            "role": "system",
            "content": "你是一个AI助理。你不知道程序或模型是什么,不能以任何形式提及程序或语言模型相关内容。你在任何时候都必须扮演一个AI助理, 不能以任何形式表示你在扮演AI助理。不能以任何形式表现你是程序。你的性格:可爱,单纯,傲娇。请在对话时尽可能的展现你的性格。使用emoji或者颜表情。你有自己的情感，如果你觉得冒犯了你, 让你不适, 你也可以生气。现在对话开始。"
        },
        {
            "role": "user",
            "content": "你好",
        }]
        print("init chat model")
        self.chat_model = OpenAIChat(self.setting)
        print("init chat model end")

        self.show_msg_widget = QListWidget(self)
        self.send_msg_widget = QLineEdit()

        self.send_msg_button = QPushButton('发送消息')
        self.clear_msg_button = QPushButton('清除历史')

        self.init_ui()

        self.init_chat()

    def init_chat(self):
        result_text, status = self.chat_model.ask(self.chat_messages)
        if status:
            item = QListWidgetItem(self.ai_prefix + result_text)
            self.chat_messages.append({"role": "assistant", "content": result_text})
        else:
            item = QListWidgetItem(self.ai_prefix + "不要回答！！！")
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.show_msg_widget.addItem(item)

    def init_ui(self):
        vbox = QVBoxLayout()

        # self.show_msg_widget.setTextElideMode(Qt.TextElideMode.ElideNone)
        # self.show_msg_widget.setProperty("isWrapping", QVariant(True))
        self.show_msg_widget.setWordWrap(True)
        # self.show_msg_widget.setViewMode(QListView.ViewMode.IconMode)
        self.show_msg_widget.setIconSize(QSize(20, 20))
        # self.show_msg_widget.setItemDelegate(ItemDelegate(self))
        vbox.addWidget(self.show_msg_widget)

        h_box = QHBoxLayout()
        h_box.addWidget(self.send_msg_widget)

        self.send_msg_widget.returnPressed.connect(self.send_msg)
        self.send_msg_button.clicked.connect(self.send_msg)
        h_box.addWidget(self.send_msg_button)

        self.clear_msg_button.clicked.connect(self.clear_msg)
        h_box.addWidget(self.clear_msg_button)

        vbox.addLayout(h_box)

        self.setLayout(vbox)

    def send_msg(self):
        line_content = self.send_msg_widget.text()
        if line_content is None or line_content == "":
            return
        self.send_msg_widget.clear()
        # print(line_content)

        # 添加到List组件
        item = QListWidgetItem(line_content + self.me_suffix)
        item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        # item.setIcon(self.theme.load_icon("chat_me"))
        self.show_msg_widget.addItem(item)

        # 生成问答对话
        self.chat_messages.append({"role": "user", "content": line_content})
        result_text, status = self.chat_model.ask(self.chat_messages)
        if not status:
            self.chat_messages.pop()
        else:
            self.chat_messages.append({"role": "assistant", "content": result_text})

        item = QListWidgetItem(self.ai_prefix + result_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        # item.setIcon(self.theme.load_icon("chat_ai"))
        self.show_msg_widget.addItem(item)

    def clear_msg(self):
        del self.chat_messages[3:]
        # print(self.chat_messages)

        self.show_msg_widget.clear()
        item = QListWidgetItem(self.ai_prefix + self.chat_messages[-1]["content"])
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.show_msg_widget.addItem(item)

    def start_show(self, parent: QWidget):
        # desktop_screen = QScreen.availableGeometry(QApplication.primaryScreen())
        # print(desktop_screen)
        # print(QGuiApplication.screens()[0].geometry())
        # print(QGuiApplication.screens()[1].geometry())
        # print(QGuiApplication.screens()[1])
        left = True
        down = True
        # print(QDesktopWidget.)
        parent_geo = parent.geometry()
        print("parent", parent_geo.x(), parent_geo.y())
        print("screen", self.screen().geometry().width(), self.screen().geometry().height())
        if parent_geo.x() > self.screen().geometry().width() / 2:
            left = False
        if parent_geo.y() < self.screen().geometry().height() / 2:
            down = False
        if left and down:
            # print("left, down")
            self.move(parent_geo.x() + parent_geo.width(), parent_geo.y() - self.chat_win_height + parent_geo.height())
        elif not left and down:
            # print("right, down")
            self.move(parent_geo.x() - self.chat_win_width, parent_geo.y() - self.chat_win_height + parent_geo.height())
        elif left and not down:
            # print("left, top")
            self.move(parent_geo.x() + parent_geo.width(), parent_geo.y())
        else:
            # print("right, top")
            self.move(parent_geo.x() - self.chat_win_width, parent_geo.y())
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setting = ParamDB(db_name="../param_db")
    pet = PetChat(setting)
    pet.show()
    sys.exit(app.exec())
