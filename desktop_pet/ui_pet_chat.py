import sys
import threading

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import *

from desktop_pet.chat_openai import OpenAIChat
from desktop_pet.param_db import ParamDB
from desktop_pet.pet_theme import PetTheme


class ProcChat(QObject):
    bg_proc = pyqtSignal(str, QPixmap, str, bool, bool)


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

        # self.show_msg_widget = QListWidget(self)
        self.show_msg_widget = QTableWidget(self)
        self.send_msg_widget = QLineEdit()

        self.send_msg_button = QPushButton('发送消息')
        self.clear_msg_button = QPushButton('清除历史')

        self.msg_signal = ProcChat()
        self.msg_signal.bg_proc.connect(self.add_msg)

        self.init_ui()

        self.init_chat()

    def init_chat(self):
        icon_chat_ai = self.theme.load_pixmap("icon_chat_ai", size=[32, 32])
        result_text, status = self.chat_model.ask(self.chat_messages)
        if status:
            self.add_msg(self.ai_prefix, icon_chat_ai, result_text, left=True)
            self.chat_messages.append({"role": "assistant", "content": result_text})
        else:
            self.add_msg(self.ai_prefix, icon_chat_ai, "不要回答！！！", left=True)

    def init_ui(self):
        vbox = QVBoxLayout()

        # self.show_msg_widget.setTextElideMode(Qt.TextElideMode.ElideNone)
        # self.show_msg_widget.setProperty("isWrapping", QVariant(True))
        # self.show_msg_widget.setItemDelegate(ChatListWidgetDelegates())
        self.show_msg_widget.setWordWrap(True)
        self.show_msg_widget.setColumnCount(3)

        # self.show_msg_widget.setViewMode(QListView.ViewMode.IconMode)
        # self.show_msg_widget.setIconSize(QSize(20, 20))
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

        msg_width = self.window().width()
        self.show_msg_widget.setColumnWidth(0, int(msg_width / 10))
        self.show_msg_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.show_msg_widget.setColumnWidth(2, int(msg_width / 10))
        self.show_msg_widget.horizontalHeader().setVisible(False)
        self.show_msg_widget.verticalHeader().setVisible(False)
        # 设置自动换行
        self.show_msg_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # 去掉网格线
        self.show_msg_widget.setShowGrid(False)

    @QtCore.pyqtSlot(str, QPixmap, str, bool, bool)
    def add_msg(self, fix: str, icon: QPixmap, msg: str, left=True, replace_last=False):
        # 插入一行
        row_count = self.show_msg_widget.rowCount()
        if replace_last and row_count > 0:
            row_count -= 1
            self.send_msg_button.setDisabled(False)
            self.send_msg_widget.setDisabled(False)
            self.clear_msg_button.setDisabled(False)
        else:
            self.show_msg_widget.insertRow(row_count)
        # 设置图标
        icon_item = QLabel()
        icon_item.setPixmap(icon)
        icon_item.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        if left:
            msg_item = QTableWidgetItem(fix + "->\n" + msg)
            msg_item.setForeground(QColor("#003371"))
            self.show_msg_widget.setCellWidget(row_count, 0, icon_item)
            msg_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        else:
            msg_item = QTableWidgetItem("<-" + fix + "\n" + msg)
            msg_item.setForeground(QColor("#424c50"))
            self.show_msg_widget.setCellWidget(row_count, 2, icon_item)
            msg_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        # 添加消息内容
        # print("add msg,", msg)
        self.show_msg_widget.setItem(row_count, 1, msg_item)
        self.show_msg_widget.scrollToBottom()

    def bg_proc(self):
        result_text, status = self.chat_model.ask(self.chat_messages)
        if not status:
            self.chat_messages.pop()
        else:
            self.chat_messages.append({"role": "assistant", "content": result_text})
        self.msg_signal.bg_proc.emit(self.ai_prefix, self.theme.load_pixmap("icon_chat_ai", size=[32, 32]), result_text, True, True)

    def send_msg(self):
        line_content = self.send_msg_widget.text()
        if line_content is None or line_content == "":
            return
        self.send_msg_widget.clear()
        self.add_msg(self.me_suffix, self.theme.load_pixmap("icon_chat_me", size=[32, 32]), line_content, left=False)

        # 生成问答对话
        self.chat_messages.append({"role": "user", "content": line_content})

        tmp_result_text = "waiting..."
        self.add_msg(self.ai_prefix, self.theme.load_pixmap("icon_chat_ai", size=[32, 32]), tmp_result_text, left=True)
        self.show_msg_widget.scrollToBottom()
        # _thread.start_new_thread(self.bg_proc, ())
        thread_bg = threading.Thread(target=PetChat.bg_proc, args=(self,))
        thread_bg.start()
        self.send_msg_button.setDisabled(True)
        self.send_msg_widget.setDisabled(True)
        self.clear_msg_button.setDisabled(True)

    def clear_msg(self):
        del self.chat_messages[3:]

        self.show_msg_widget.setRowCount(0)
        self.add_msg(self.ai_prefix, self.theme.load_pixmap("icon_chat_ai", size=[32, 32]),
                     self.chat_messages[-1]["content"], left=True)

    def start_show(self, parent: QWidget):
        left = True
        down = True
        parent_geo = parent.geometry()
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
