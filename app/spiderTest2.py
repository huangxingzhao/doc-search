import asyncio
import json
from datetime import datetime, timedelta

import aiohttp
import requests
from fake_useragent import UserAgent
from playwright.async_api import async_playwright, expect
from apscheduler.schedulers.blocking import BlockingScheduler

from app.db.SpiderDocument import SpiderDocument
from app.db.SpiderDocumentCrud import spiderDocumentCrud
from app.db.base.config import scheduler
from app.db.base.log import spider_logger

# response = requests.get(
#     'https://dps.kdlapi.com/api/getdps/?secret_id=ocyzbirs58tubqbbaln4&num=1&signature=vdjp3lf92xxa028ewwagrgh6p79de7hm&pt=1&format=json&sep=1')
# data = response.json()
# proxy = data["data"]["proxy_list"][0]

# page.goto("http://toutiao.com/a7297130195817939490/?app=news_article&is_hit_share_recommend=0")
# page.wait_for_selector('div.article-content')
# article = page.query_selector('div.article-content')
# print(article.text_content())

doc_list_url = ""


async def on_response(response):

    if "www.toutiao.com/api/pc/list/feed" in response.url and 'channel_id=94349549395' not in response.url:
        print(f"urlll{response.url}")
        text_ = await response.text()
        await print_rsp_data(json.loads(text_))
        # tempm(response.url)


server_url = 'http://localhost:8000/document/save'


def cuo2DateimIso(date_str):
    return datetime.fromtimestamp(date_str).isoformat()


async def tempm(url):
    response = requests.get(url)
    # 检查响应状态码，确保请求成功
    if response.status_code == 200:
        # 将返回内容解析为JSON对象
        json_response = response.json()
        await print_rsp_data(json_response)
    else:
        print(f"请求失败，状态码：{response.status_code}")


async def send_async_post_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.text()


async def print_rsp_data(json_response):
    # 获取当前时间
    current_time = datetime.now()

    # 计算3天前的时间
    three_days_ago = current_time - timedelta(days=3)


    for i in json_response['data']:
        if "article_url" in i:
            fromtimestamp = datetime.fromtimestamp(i['publish_time'])
            # if fromtimestamp < three_days_ago:
            #     continue
            data = {'title': i['title'], 'article_url': i['article_url'], 'read_count': i['read_count'],
                    'publish_time': fromtimestamp.isoformat(), 'like_count': i.get('like_count'),
                    'comment_count': i['comment_count'], 'behot_time': cuo2DateimIso(i['behot_time']),
                    'source': 'toutiao', 'domain': '测试'}

            doc: SpiderDocument = SpiderDocument(
                source="toutiao",
                domain="娱乐",
                title=i['title'],
                article_url=i['article_url'],
                read_count=i['read_count'],
                like_count=i.get('like_count'),
                comment_count=i['comment_count'],
                publish_time=datetime.fromtimestamp(i['publish_time']),
                behot_time=datetime.fromtimestamp(i['behot_time'])
            )
            print("search_doc6")

            spider_logger.debug(f"录入文章{data}")
            await spiderDocumentCrud.save_doc(doc)
            # await send_async_post_request(server_url, data=json.dumps(data))
            # requests.post(server_url, data=json.dumps(data))



async def search_doc():
    count = await spiderDocumentCrud.get_doc_count()
    spider_logger.debug("开始执行爬虫任务,当前文章数量为" + str(count))
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome', headless=True)
        # proxy={"server": "http://" + proxy, "username": "d1081643637",
        #        "password": "dozb0uu1"})
        context = await browser.new_context(user_agent=UserAgent().random)
        page = await context.new_page()
        # # 关闭Webdriver属性
        js = """
                Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
                """
        await page.add_init_script(js)
        try:
            await page.goto("https://www.toutiao.com/")

            page.on('response', on_response)
            # fixme
            await asyncio.sleep(8)
            # await page.wait_for_function('() => document.querySelectorAll("div.feed-more-nav-item").length > 0', timeout=15000)
            # await page.wait_for_function('() => document.querySelectorAll("div.feed-default-nav-item").length > 0', timeout=15000)

            # await page.wait_for_selector('div.feed-more-nav-item')
            # await page.wait_for_selector('div.feed-default-nav-item')
            nav_list = (await page.query_selector_all('div.feed-more-nav-item')) + (
                await page.query_selector_all('div.feed-default-nav-item'))
            for nav in nav_list:
                content = await nav.text_content()
                print(content)
                if "娱乐" in content:
                    await page.evaluate('element => element.click()', nav)
                    # fixme
                    await asyncio.sleep(8)
                    break
            print("search_doc4")
        except Exception as e:
            spider_logger.error(
                f"search_doc error {e}"
            )
            pass

        # ---------------------
        await context.close()
        await browser.close()
    spider_logger.debug("爬虫任务执行结束")
    if count == await spiderDocumentCrud.get_doc_count():
        spider_logger.error("爬虫任务执行结束,未发现新文章")




# loop.run_until_complete(search_doc())


# asyncio.sleep(50)
# async def temp():
#     asyncio.run(search_doc())
#     asyncio.run(search_doc())

# asyncio.run(temp())

# scheduler = BlockingScheduler()
# scheduler.add_job(job_function, 'interval', seconds=30)
# scheduler.start()
# # print([[i.text_content(),i.get_attribute('href')] for i in links])

# https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc&_signature=_02B4Z6wo00901Xdb59gAAIDB91kdmPtzXb13b8NAADihxuv8rSdFSbmRgZEye9ARZg3iLhmEwrEIfa1-ktbKGquEEPJZ4rXhr4B1rIlocUQOZC.DJPBXzZ950VXHdjEOJNbENxB8CuFWWfTn27
