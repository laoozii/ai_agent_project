import os
import logging

from config.settings import settings
from agent.simple_agent import SimpleAgent

def setup_directories():
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    os.makedirs(settings.DATA_DIR, exist_ok=True)

def setup_logging():
    """
    配置日志系统。
    """

    log_file = os.path.join(settings.LOG_DIR, "app.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )   

def main():
    """
    程序主入口。
    """
    try:
        settings.validate_required()

    except ValueError as e:
        print(f"配置错误: {e}")
        return

    setup_directories()
    setup_logging()

    logging.info("AI Agent 程序启动")

    agent = SimpleAgent()

    print("AI Agent 已启动，输入 exit 退出。")

    while True:
        user_input = input("\n用户：")

        if user_input.lower() in ["exit", "quit"]:
            logging.info("AI Agent 程序退出")
            print("程序已退出。")
            break

        logging.info(f"用户输入：{user_input}")

        try:
            response = agent.run(user_input)
            logging.info(f"Agent 回复：{response}")
            print(f"\nAgent：{response}")

        except Exception as e:
            logging.error(f"程序运行出错：{e}")
            print(f"程序运行出错：{e}")


if __name__ == "__main__":
    main()