import sys
import itertools 
import threading
import time

class Signal:
	go = True 

def spin(msg, signal):
	std_write, std_flush = sys.stdout.write, sys.stdout.flush
	for char in itertools.cycle('|/-\\'):
		status = char + ' ' + msg
		std_write(status)
		std_flush()
		std_write('\x08' * len(status))
		time.sleep(0.1)
		if not signal.go:
			break
	std_write(' ' * len(status) + '\x08' * len(status))

def slow_function():
	# pretending there were io process!
	time.sleep(3)
	return 42

def supervisor():
	signal = Signal()
	spinner = threading.Thread(
						target=spin,
						args=('thinking!', signal))
	print("spinner object:", spinner)
	spinner.start()
	res = slow_function()
	signal.go = False
	spinner.join()
	return res 

def main():
	res = supervisor()
	print("Answer:", res)

if __name__ == "__main__":
	main()
