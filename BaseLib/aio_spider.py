# asyncio spyder, store and deduplicate
import asyncio
import aiohttp
import aiomysql
import re
from pyquery import PyQuery

start_url = 'http://blog.jobbole.com/'
waiting_urls = []
seen_urls = set()
seen_titles = set()
stopping = False

sem = asyncio.Semaphore(5)
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

async def fetch(url, session):
    async with sem:
    	try:
    		async with session.get(url) as resp:
    			# print(resp.status)
    			print('url_status:{}'.format(resp.status))
    			if resp.status in [200, 201]:
    				data = await resp.text()
    				return data
    	except Exception as e:
    			print(e)


def extract_urls(html):
    urls = []
    pq = PyQuery(html)
    for link in pq.items('a'):
        url = link.attr('href')
        if url and url.startswith('http') and url not in seen_urls:
            urls.append(url)
            waiting_urls.append(url)
    return urls

async def init_urls(session):
	html = await fetch(start_url, session)
	extract_urls(html)

async def article_handler(url, session, pool):
    html = await fetch(url, session)
    seen_urls.add(url)
    extract_urls(html)
    try:
        pq = PyQuery(html)
        title = pq('title').text()
        if title not in seen_titles:
            seen_titles.add(title)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"INSERT INTO aio_test(title, url) values('{title}','{url}')")
                    print(cur.description)
                    print(title, '已经入库！！！')
        await pool.wait_closed()
    except Exception as e:
        print(e)


async def consumer(pool):
	# while not stopping:
    async with aiohttp.ClientSession(headers = headers) as session:
        while True:
            if len(waiting_urls) == 0:
                await asyncio.sleep(0.5)
                continue
            url = waiting_urls.pop()
            print('start get url:{}'.format(url))
            if re.match(r'http://blog.jobbole.com/\d+/.*?', url):
                if url not in seen_urls:
                    asyncio.ensure_future(article_handler(url, session, pool))
                    # asyncio.create_task(article_handler(url, session, pool))
                    await asyncio.sleep(0.5)

async def main(loop):
	# wait connect building with mysql
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
									  user='root', password='yangzhikai668',
									  db='spider', loop=loop, charset='utf8',
									  autocommit=True)

    async with aiohttp.ClientSession(headers=headers) as session:
        await init_urls(session)
        seen_urls.add(start_url)

    asyncio.create_task(consumer(pool))

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	asyncio.ensure_future(main(loop))
	loop.run_forever()
	# asyncio.run(main(loop))