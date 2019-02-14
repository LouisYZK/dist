import asyncio

import matplotlib.pyplot as plt
import numpy as np

from method import (aiomultiprcocess_test, async_aiohttp_sigle_thread,
                    async_requests_processpool, async_requests_threadpool,
                    requests_processpool, requests_threadpool)

NUMBERS = 20

methods = [
    aiomultiprcocess_test,
    async_aiohttp_sigle_thread,
    async_requests_processpool,
    async_requests_threadpool,
    requests_processpool,
    requests_threadpool
]
res = {method.__name__: [] for method in methods}

def show_res():
    markers = ['.', 'o', '*', 'p', '^', 'h']
    plt.style.use('ggplot')
    for (method_name, data), marker in zip(res.items(), markers):
        plt.plot(range(1, NUMBERS),
                data,
                label=method_name,
                marker=marker)
    plt.legend()
    plt.show()

for i in range(1,NUMBERS):
    for method in methods:
        try:
            if method.__name__.startswith('requests'):
                res[method.__name__].append(
                    method(num=range(i*6)).main()
                )
            else:
                res[method.__name__].append(
                    asyncio.run(method(num=range(i*6)).main())
                )
        except Exception:
            show_res()

show_res()
