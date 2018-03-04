#from dateutil.relativedelta import relativedelta

def time_phrase(number, duration, relation):
	# assume duration is days
	if relation == "after":
		direction = 1
	elif relation == "before":
		direction = -1
	return int(number) * direction