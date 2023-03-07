from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QCheckBox

from desktop_pet.param_db import ParamDB


class UISetting(QWidget):
    def __init__(self, setting: ParamDB, parent=None):
        super().__init__(parent=parent)
        self.setting = setting

        self.ack_button = QPushButton('确定')
        self.cancel_button = QPushButton('取消')
        self.param_widget = QTableWidget(self)

        self.setting_win_width = int(self.setting.setting_get("setting_win_width"))
        self.setting_win_height = int(self.setting.setting_get("setting_win_height"))
        self.resize(self.setting_win_width, self.setting_win_height)

        self.init_ui()
        self.setting_list = {
            "theme_name": {
                "type": "edit",
                "show_name": "主题 ->",
            },
            "none_0": {

            },
            "openai_model": {
                "type": "edit",
                "show_name": "OpenAI Model ->",
            },
            "openai_api_key": {
                "type": "edit",
                "show_name": "OpenAI Key ->",
            },
            "openai_organization": {
                "type": "edit",
                "show_name": "OpenAI Org ->",
            },
            "openai_proxy": {
                "type": "edit",
                "show_name": "OpenAI 代理 ->",
            },
            "openai_role": {
                "type": "edit",
                "show_name": "OpenAI 角色 ->",
            },
            "openai_character": {
                "type": "edit",
                "show_name": "OpenAI 性格 ->",
            },
            "chat_single_item": {
                "type": "check",
                "show_name": "单次问答 ->",
            },
            "chat_use_test": {
                "type": "check",
                "show_name": "测试 ->",
            },
            "none_1": {

            },
            "chat_ai_prefix": {
                "type": "edit",
                "show_name": "AI前缀 ->",
            },
            "chat_me_prefix": {
                "type": "edit",
                "show_name": "ME前缀 ->",
            },
        }
        self.add_setting()

    def init_ui(self):
        self.setStyleSheet("background-color:#f0fcff;border-radius:15px")
        self.setWindowTitle("Setting")
        self.setWindowFlags(
            Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            # | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowStaysOnTopHint
            # | Qt.WindowType.SubWindow
        )
        self.setAutoFillBackground(False)

        # 各种参数的设置
        vbox = QVBoxLayout()

        table_qss = '''
        QTableWidget
        {
            background-color:#e3f9fd;
            border-radius:15px;
            outline:none;
            border:none;
        }
        QTableWidget::item::selected
        {
            color:#801dae;
            background:#e3f9fd;
            outline:none;
            border:none;
        }
        '''
        self.param_widget.setStyleSheet(table_qss)
        win_width = self.width()
        self.param_widget.setColumnCount(3)
        self.param_widget.setColumnWidth(0, int(win_width / 4))
        self.param_widget.setColumnWidth(1, int(win_width / 40))
        self.param_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.param_widget.horizontalHeader().setVisible(False)
        self.param_widget.verticalHeader().setVisible(False)
        # 去掉网格线
        self.param_widget.setShowGrid(False)
        self.param_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        vbox.addWidget(self.param_widget)

        h_box = QHBoxLayout()

        self.ack_button.setFixedWidth(50)
        self.ack_button.setStyleSheet("background-color:#d6ecf0;border-radius:5px")
        self.ack_button.clicked.connect(self.ack)
        h_box.addWidget(self.ack_button)
        self.cancel_button.setFixedWidth(50)
        self.cancel_button.setStyleSheet("background-color:#d6ecf0;border-radius:5px")
        self.cancel_button.clicked.connect(self.cancel)
        h_box.addWidget(self.cancel_button)

        vbox.addLayout(h_box)
        self.setLayout(vbox)

    def add_setting(self):
        for key in self.setting_list:
            item = self.setting_list[key]
            row_count = self.param_widget.rowCount()
            self.param_widget.insertRow(row_count)
            if key.startswith("none"):
                continue

            label = QLabel()
            label.setText(item["show_name"])
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.param_widget.setCellWidget(row_count, 0, label)
            if item["type"] == "edit":
                value = QLineEdit()
                value.setText(self.setting.setting_get(key))
                self.param_widget.setCellWidget(row_count, 2, value)
                item["widget"] = value
            elif item["type"] == "check":
                value = QCheckBox()
                value.setChecked(self.setting.setting_get(key) == "True")
                self.param_widget.setCellWidget(row_count, 2, value)
                item["widget"] = value

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
            self.move(parent_geo.x() + parent_geo.width(),
                      parent_geo.y() - self.setting_win_height + parent_geo.height())
        elif not left and down:
            # print("right, down")
            self.move(parent_geo.x() - self.setting_win_width,
                      parent_geo.y() - self.setting_win_height + parent_geo.height())
        elif left and not down:
            # print("left, top")
            self.move(parent_geo.x() + parent_geo.width(), parent_geo.y())
        else:
            # print("right, top")
            self.move(parent_geo.x() - self.setting_win_width, parent_geo.y())
        self.show()

    def cancel(self):
        self.hide()

    def ack(self):
        for key in self.setting_list:
            if key.startswith("none"):
                continue
            item = self.setting_list[key]
            # print(item)
            if item["type"] == "edit":
                text_value = item["widget"].text()
                # print(text_value)
                self.setting.setting_set(key, str(text_value), exist=True)
            elif item["type"] == "check":
                # print(item["widget"].isChecked())
                self.setting.setting_set(key, str(item["widget"].isChecked()), exist=True)
        self.hide()
