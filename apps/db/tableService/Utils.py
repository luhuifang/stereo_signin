import string
import random
def get_randstr(prefix=None, length=32):
	ran_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
	if prefix:
		UUID = '{0}_{1}'.format(prefix, ran_str)
	else:
		UUID = ran_str
	return UUID