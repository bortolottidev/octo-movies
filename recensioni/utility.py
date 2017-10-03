from django.contrib.auth.models import Group
from . import models
from LD_Proj.utility import errore

officialGroup = "Recensori ufficiali"

# La funzione analizza tutti i commenti di una data recensione, alla
# ricerca di quelli lasciati dal nostro self.user
def commentsAnalyzer(self, recensione, found):
	# Se la recensione è scritta dal nostro user è positiva
	if recensione.autore.id == self.getUserId():
		return True, 1
	voto = 0
	found = False
	for commento in recensione.commento_set.all():
		if commento.autore.id == self.getUserId():
			found = True
			if (commento.voto == True):
				voto = 1
			elif (commento.voto == False):
				voto = 0
			else: 
				voto = 0
	return (found, voto)

# Funzione che restituisce le ultime cinque recensioni pubblicate ufficialmente
# (scritte da recensori appartenenti al gruppo dei recensori ufficiali) 
def latestOfficial():
	try:
		group = Group.objects.get(name=officialGroup)
		member = group.user_set.all()
	except:
		errore("Errore in: latestOfficial()")
		return []
	else:
		officialRec = []
		for rec in models.Recensione.objects.order_by('-pub_date'):
			if rec.autore in member:
				officialRec.append(rec)
		return officialRec[:5]
