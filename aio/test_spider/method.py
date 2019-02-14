import time
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import aiohttp
from aiomultiprocess import Pool

URL = 'http://httpbin.org/get?a={}'

async def fetch_async(a):
    async with aiohttp.request('GET', URL.format(a)) as r:
        data = await r.json()
    return data['args']['a']

def fetch(a):
        r = requests.get(URL.format(a))
        return r.json()['args']['a']


class requests_threadpool():
    def __init__(self, num):
        self.num = num

    def main(self):
        start = time.time()
        with ThreadPoolExecutor(max_workers=3) as executor:
            for num, result in zip(self.num, executor.map(fetch, self.num)):
                print('fetch({}) = {}'.format(num, result))

        # print('Use requests+ThreadPoolExecutor cost: {}'.format(time.time() - start))
        return time.time() - start

class requests_processpool():
    def __init__(self, num):
        self.num = num

    def main(self):
        start = time.time()
        with ProcessPoolExecutor(max_workers=3) as executor:
            for num, result in zip(self.num, executor.map(fetch, self.num)):
                print('fetch({}) = {}'.format(num, result))

        print('Use requests+ProcessPoolExecutor cost: {}'.format(time.time() - start))
        return time.time() - start

class async_requests_threadpool():

    def __init__(self, num):
        self.num = num

    async def aiohttp_async(self):
        with ThreadPoolExecutor(max_workers=3) as executor:
            for num, result in zip(self.num, executor.map(fetch, self.num)):
                print('fetch({}) = {}'.format(num, result))

    async def main(self):
        start = time.time()
        await self.aiohttp_async()
        return time.time() - start


class async_requests_processpool():
    def __init__(self, num):
        self.num = num

    async def aiohttp_async(self):
        with ProcessPoolExecutor(max_workers=3) as executor:
            for num, result in zip(self.num, executor.map(fetch, self.num)):
                print('fetch({}) = {}'.format(num, result))

    async def main(self):
        start = time.time()
        await self.aiohttp_async()
        return time.time() - start

class async_aiohttp_sigle_thread():
    def __init__(self, num):
        self.num = num

    async def fetch_async(self, a):
        async with aiohttp.request('GET', URL.format(a)) as r:
            data = await r.json()
        return data['args']['a']

    async def aiohttp_async(self):
        tasks = [self.fetch_async(i) for i in self.num]
        res = await asyncio.gather(*tasks)
        return res

    async def main(self):
        start = time.time()
        res = await self.aiohttp_async()
        for res_item , num in zip(res, self.num):
            print(f'fetch({num}) = {res_item}')
        print(f'aiohttp+asyncio uses {time.time() - start} s......')
        return time.time() - start

class async_aiohttp_threadpool():
    pass

class async_aiohttp_processpool():
    pass

class ruia_test():
    pass

class aiomultiprcocess_test():
    def __init__(self, num):
        self.num = num

    async def main(self):
        start = time.time()
        async with Pool() as pool:
            result = await pool.map(fetch_async, self.num)
        for res_item, i in zip(result, self.num):
            print(f'fetch{i} = {res_item}')
        print(f'aiomultiprocess uses:{time.time() - start}s')
        return time.time() - start

# asyncio.run(aiohttp_sigle_thread(num=range(10)).main())
# requests_threadpool(num=range(10)).main()
# asyncio.run(async_request_threadpool(num=range(10)).main())

# requests_processpool(num=range(10)).main()

# asyncio.run(aiomultiprcocess_test(num=range(30)).main())