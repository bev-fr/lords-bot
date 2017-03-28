from multiprocessing import Process

def background(func):
	def threader(*args, **kwargs):
		p = Process(
			target = func,
			args = [*args],
			kwargs = {**kwargs},
		)
		p.start()
	return threader
