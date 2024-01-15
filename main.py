# This is a sample Python script.
import asyncio

from app.db.base.config import scheduler
from app.spiderTest2 import search_doc

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

loop = asyncio.get_event_loop()

def doc_search_job():

    # asyncio.run(search_doc())
    loop.run_until_complete(search_doc())


scheduler.add_job(doc_search_job, 'interval', seconds=60, id='doc_search_job', replace_existing=True)
# # 启动调度器

async def start_job():
    try:
        scheduler.start()
        while True:
            await asyncio.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        # 当收到中断信号或系统退出信号时停止调度器
        loop.close()
        scheduler.shutdown()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # asyncio.run(start_job())
    print("hello mabi")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
