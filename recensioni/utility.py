from django.contrib.auth.models import Group
from . import models

officialGroup = "Recensori ufficiali"

# La funzione analizza tutti i commenti di una data recensione, alla
# ricerca di quelli lasciati dal nostro self.user
def commentsAnalyzer(self, recensione, found):
	# Se la recensione è scritta dal nostro user è positiva
	if recensione.autore.id == self.getUserId():
		return True, 1
	voto = 0
	found = False
	# Ottimizzabile ordinando i risultati dall'ultimo
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
	officialRec = []
	officialUser = Group.objects.get(name=officialGroup).user_set.all()
	for rec in models.Recensione.objects.order_by('-pub_date'):
		if rec.autore in officialUser:
			officialRec.append(rec)
	return officialRec[:5]
