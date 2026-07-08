from openai import OpenAI
from config.settings import settings

class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.model_name = settings.MODEL_NAME
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

    def chat(self, user_message: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "你是一个辅助用户学习的助手。请根据用户的输入提供有用和相关的回答。"
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                max_tokens=1000,
            )
        except Exception as e:
            raise RuntimeError(f"DeepSeek API 请求失败: {e}")
        
        try:
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"DeepSeek API 响应失败: {e}")