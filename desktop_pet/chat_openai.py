import openai

from desktop_pet.param_db import ParamDB


class OpenAIChat:
    def __init__(self, setting: ParamDB):
        self.setting = setting
        self.model = self.setting.setting_get("openai_model")
        openai.organization = self.setting.setting_get("openai_organization")
        openai.api_key = self.setting.setting_get("openai_api_key")
        openai.proxy = self.setting.setting_get("openai_proxy")

    def ask(self, messages):
        return "不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！不要回答！！！", True
        # try:
        #     response = openai.ChatCompletion.create(
        #         model=self.model,
        #         messages=messages,
        #         temperature=1)
        #     return response['choices'][0]['message']['content'], True
        # except Exception as e:
        #     print(e)
        #     return "不要回答！！！", False
