from django.contrib.auth  import authenticate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from LD_Proj.utility import objectExist
from recensioni import models
from .models import UserProfile

from distance import hamming
from operator import itemgetter

# Soglia sopra la quale la similarità viene considerata.
# I "Potrebbero interessarti.." casuali non piacciono a nessuno.
THRESHOLD = 0.15

officialGroup = 'Recensori ufficiali'

# Check di controllo su myUser. Fa parte del gruppo recensori pro?
def isOfficial (myUser):	
	group = Group.objects.get(name=officialGroup).user_set.all()
	for user in group:
		if user == myUser:
			return True
	return False

# Ritorna la lista dei film suggeriti per un certo user, 
# in base all'utente più simile al nostro myUser
def suggestFilm (myUser):
	suggList = []
	if myUser:
		nearbyUser = None
		try:
			if myUser.is_anonymous():
				raise Exception(333, "User anonymous")
			nearbyUser = closestProfile(myUser)
			myList = eval(getattr(myUser, "userprofile").getVect())
			nearbyList = eval(getattr(nearbyUser, "userprofile").getVect())
			count = 0
			for i in models.Recensione.__allRec__():
				#print("Recensione - ", i, " - me ", myList[count], " - lui", nearbyList[count])
				if (myList[count] != nearbyList[count]):
					suggList.append(i)
				# Più corretto, ma troppo restrittivo nel nostro toy db
				#if ((myList[count] == 0) and (nearbyList[count] == 1)):
				#	suggList.append(i)
				count = count+1
		except:
			return []
		return suggList
	else:
		return suggList

# Restituisce il profilo più simile a user1, attraverso l'analisi
# del suo vettore profilo.
# Questa funzione necessita di essere chiamata dentro un "try:"
def closestProfile(user1):
	closest = {}
	method = "userprofile"
	vect1 = eval(getattr(user1, method).getVect())
	if (user1.id == anonymous()):
		raise Exception(112, "Il nostro user è anonimo")
	if not objectExist(user1, method):
		raise Exception(111, "Il tuo user non ha profilo")
	for user2 in User.objects.all():
		if (user2.id == user1.id) or (user2.id == anonymous()) : 
			closest[user2] = 0
			# L'utente anonimo è qualcosa di costruito casualmente,
			# da molti utenti, non ha senso confrontarlo con un user singolo
		else :
			if objectExist(user2, method):
					vect2 = eval(getattr(user2, method).getVect())
					# similarity = 1 - hamming distance normalizzata
					sim = 1 - hamming(vect1, vect2, normalized = True)
					#print(str(user2)+" sim: "+str(sim))
					if (sim != 1) and (user2.userprofile.check):
						# Rimuoviamo gli utenti uguali al nostro.. Non ci danno 
						# informazioni utili. è un limit dell'algoritmo.
						closest[user2] = sim
			# else: l'user in questione non ha profilo..
	if closest :
		#for user in closest: print(user1.userprofile.getVect(), user.userprofile.getVect())
		# Una volta messe le similarità in ordine decrescente, è facile trovare
		# il più simile..
		userFound, maxVal = next( iter(
			sorted(closest.items(), key=itemgetter(1), reverse=True)	) 	)
		#print("Utente più simile a "+str(user1)+" = "+str(userFound)+str(maxVal))
		#print("Check vettori:", user1.userprofile.getVect(), userFound.userprofile.getVect())
		
		if (maxVal < THRESHOLD):
			raise Exception(220, "User più vicino sotto soglia threshold")
		if (maxVal >= THRESHOLD):
			return userFound
		raise Exception(221, "Nessun utente vicino")
	else:
		raise Exception(222, "Impossibile trovare vettori utenti")
	
# Definisco l'utente anonimo in realtà come un utente fittizio
# Restituisco il suo id per evitare problemi di serializzazione (???)
def anonymous():
	userAnon = User.objects.get(username="userAnon")
	return userAnon.id
