from multiprocessing.managers import BaseManager
from threading import Thread
from multiprocessing import Process
from queue import Queue
import numpy as np

class ParallelDataGetter(Thread):
    def __init__(self, port):
        super().__init__()
        self._port = port
        self.data = Queue(maxsize=2000)

        class InferenceMemoryManager(BaseManager):
            pass

        InferenceMemoryManager.register(
            'get_dataqueue', callable=lambda: self.data)

        m = InferenceMemoryManager(address=('', self._port), authkey=b'abc')
        self._agent_server = m.get_server()

    def run(self):
        """Start listening in thread."""
        # print(f"$$$$$$$$$$$$$$$$$$${self.data.get(timeout = 100)}")
        self._agent_server.serve_forever()

class ParallelDataWorker(Process):
	def __init__(self, port, name):
		self._port = port 
		self.worker_name = name 
		super().__init__()
		class InferenceMemoryManager(BaseManager):
			pass
		InferenceMemoryManager.register('get_dataqueue')
		m = InferenceMemoryManager(address = ('localhost', self._port), authkey = b'abc')
		m.connect()
		self.data = m.get_dataqueue()
		print(f'#####################{self.data}')
		print('worker has been created!')

	def run(self):
		while True:
			rand_data = np.random.randint(100)
			print(f"{rand_data} are put in by {self.worker_name} !")
			self.data.put(rand_data)
			if self.data.full():
				break

if __name__ == '__main__':
	print('start Putting Data !!!-------------------------')
	getter = ParallelDataGetter(9000)
	getter.start()
	workers = []
	for i in range(4):
		workers.append(ParallelDataWorker(9000,
					'Worker_{}'.format(i)),
					)

	for worker in workers:
		worker.start()

	for worker in workers:
		worker.join()
	print('-----------------Output data--------------------',getter.data)
	while not getter.data.empty():
		print('**********^^^',getter.data.get(),'^^^^^^***************')
	getter.join()

