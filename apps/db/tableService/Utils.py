import string
import random
def get_randstr(prefix):
	ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
	UUID = '{0}_{1}'.format(prefix, ran_str)
	return UUID