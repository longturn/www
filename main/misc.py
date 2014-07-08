from longturn.old.models import OldGame, OldJoined, OldUser
from longturn.game.models import Joined

# arg - new user
def timesplayed(user):
	olduser = getolduser(user)
	times = 0
	times += Joined.objects.filter(user=user).count()
	times += oldtimesplayed(olduser)
	return times

# arg - old user
def oldtimesplayed(user):
	times = 0
	if user:
		times += OldJoined.objects.filter(user=user).count()
	return times

# arg - new user
def timeswon(user):
	olduser = getolduser(user)
	times = 0
	times += Joined.objects.filter(user=user, is_winner=True).count()
	times += oldtimeswon(olduser)
	return times

# arg - old user
def oldtimeswon(user):
	times = 0
	if user:
		times += OldJoined.objects.filter(user=user, is_winner=True).count()
	return times

# arg - new user
def timesidle(user):
	olduser = getolduser(user)
	times = 0
	times += Joined.objects.filter(user=user, is_idler=True).count()
	times += oldtimesidle(olduser)
	return times

# arg - old user
def oldtimesidle(user):
	times = 0
	if user:
		times += OldJoined.objects.filter(user=user, is_idler=True).count()
	return times

def getolduser(user):
	olduser = None
	try:
		olduser = OldUser.objects.get(activeuser=user)
	except:   
		pass
	return olduser

def getoldjoineds(user):
	olduser = getolduser(user)
	return list(OldJoined.objects.filter(user=olduser))
