import os
import logging

from config.settings import settings
from agent.simple_agent import SimpleAgent
from session.store import SessionStore


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

    store = SessionStore(settings.DATA_DIR)
    agent = SimpleAgent(store)

    print("AI Agent 已启动，输入 exit 退出。")

    while True:
        user_input = input("\n用户：")

        if user_input.lower() in ["exit", "quit", "/exit"]:
            logging.info("AI Agent 程序退出")
            print("程序已退出。")
            break

        if user_input.startswith("/session"):

            parts = user_input.split()

            if len(parts) == 1:
                print("用法： /session new <title> - 创建新会话\n /session list - 列出所有会话\n /session load <session_id> - 加载指定会话")
                continue

            if parts[1] == "new":
                if len(parts) < 3:
                    print("请提供会话标题。用法： /session new <title>")
                    continue
                
                if len(parts) > 2:
                    title = " ".join(parts[2:])
                    session = store.create_session(title)
                    store.save_session(session)
                    store.set_current_session_id(session["session_id"])
                    print(f"已创建新会话，ID: {session['session_id']}, 标题: {session['title']}")
                    continue
                
            elif parts[1] == "list":
                sessions = store.list_sessions()
                if not sessions:
                    print("没有找到任何会话。")
                else:
                    print("会话列表：")
                    for session_id, title in sessions:
                        print(f"ID: {session_id}, 标题: {title}\n")
                continue

            elif parts[1] == "load":
                if len(parts) < 3:
                    print("请提供会话ID。用法： /session load <session_id>")
                    continue
                session_id = parts[2]
                
                try:
                    session = store.load_session(session_id)
                    store.set_current_session_id(session_id)
                    print(f"已加载会话，ID: {session['session_id']}, 标题: {session['title']}")
                except ValueError:
                    print("会话不存在。")

                continue

            elif parts[1] == "switch":
                if len(parts) < 3:
                    print("请提供会话ID。用法： /session switch <session_id>")
                    continue
                session_id = parts[2]
                
                try:
                    store.switch_session(session_id)
                    print(f"已切换到会话，ID: {session_id}")
                except ValueError:
                    print("会话不存在。")
                continue

            elif parts[1] == "rename":
                if len(parts) < 4:
                    print("请提供会话ID和新标题。用法： /session rename <session_id> <new_title>")
                    continue
                session_id = parts[2]
                new_title = " ".join(parts[3:])
                
                try:
                    store.rename_session(session_id, new_title)
                    print(f"已重命名会话，ID: {session_id}, 新标题: {new_title}")
                except ValueError:
                    print("会话不存在。")
                continue

            elif parts[1] == "delete":

                if len(parts) < 3:
                    print("请提供会话ID。用法： /session delete <session_id>")
                    continue
                session_id = parts[2]
                
                try:
                    store.delete_session(session_id)
                    print(f"已删除会话，ID: {session_id}")
                except ValueError:
                    print("会话不存在。")
                continue
            print ("未知的 /session 命令。可用命令： new, list, load, switch, rename, delete")
            continue
        
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