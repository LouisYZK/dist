import requests
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

URL = 'http://httpbin.org/get?a={}'

pairs = range(10)

def get_csv(pair, out_q):
    res = requests.get(URL.format(pair))
    out_q.put(res.json()['args']['a'])


# with ThreadPoolExecutor(max_workers=3) as executor:
#     res_q = Queue()
#     # for pair, res in zip(pairs, executor.map(get_csv, [pairs, res_q])):
#     #     print('res')
#     for pair in pairs:
#         executor.submit(get_csv, pair, res_q)

# # print(res_q.get())
# while not res_q.empty():
#     print(res_q.get())


