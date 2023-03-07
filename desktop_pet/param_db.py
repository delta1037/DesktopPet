import sqlite3

from desktop_pet import DB_NAME


class ParamDB:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.init_table()

    def init_table(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS setting (key TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL );''')
        self.conn.commit()

    def kv_get(self, key):
        sql = '''SELECT key,value FROM setting WHERE key="{}"'''.format(key)
        cur = self.conn.cursor()
        result = cur.execute(sql).fetchall()
        if len(result) <= 0:
            return None
        elif len(result) == 1:
            return result[0][1]
        else:
            print("[WARN] database error")
            return result[0][1]

    def kv_set(self, key, value, exist=False):
        if exist:
            sql = '''UPDATE setting SET value = "{}" WHERE key="{}"'''.format(value, key)
        else:
            sql = '''INSERT INTO setting (key, value) VALUES ("{}","{}")'''.format(key, value)
        cur = self.conn.cursor()
        # print(sql)
        cur.execute(sql)
        self.conn.commit()

    def setting_set(self, key, value, exist=False):
        self.kv_set(key=key, value=value, exist=exist)

    def setting_get(self, key):
        ret = self.kv_get(key)
        if ret is not None:
            return ret

        set_key = key
        set_value = ""
        if set_key == "theme_name":
            set_value = "default"
        elif set_key == "main_win_width":
            set_value = 128
        elif set_key == "main_win_height":
            set_value = 128
        elif set_key == "openai_model":
            set_value = "gpt-3.5-turbo"
        elif set_key == "openai_organization":
            set_value = "xxx"
        elif set_key == "openai_api_key":
            set_value = "xxx"
        elif set_key == "openai_role":
            set_value = "AI助理"
        elif set_key == "openai_character":
            set_value = "可爱,单纯"
        elif set_key == "openai_proxy":
            set_value = "http://127.0.0.1:8080"
        elif set_key == "chat_ai_prefix":
            set_value = "三体 -> "
        elif set_key == "chat_me_prefix":
            set_value = " <- 叶文洁"
        elif set_key == "chat_win_width":
            set_value = 600
        elif set_key == "chat_win_height":
            set_value = 400
        elif set_key == "chat_single_item":
            set_value = "True"
        elif set_key == "chat_use_test":
            set_value = "False"
        elif set_key == "setting_win_width":
            set_value = 300
        elif set_key == "setting_win_height":
            set_value = 450
        # 设置默认值
        self.kv_set(set_key, set_value, exist=False)
        return set_value
