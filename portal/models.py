from django.db.models import Model, BooleanField, OneToOneField, CharField
from django.contrib.auth.models import User
from recensioni.utility import commentsAnalyzer
from recensioni import models

# Voti richiesti per inserire l'utente nel sistema di vicinanza.
# Più l'utente posta voti e commenti e più ci aspettiamo sia accurata la
# sua profilazione.
# Attualmente estremamente basso a causa del mio database fittizio
VOTES_REQUIRED = 2

# Profilo utente
# simVect: 	raccoglie in un vettore booleano tutti i commenti lasciati
#			1 = commento positivo a recensione, 0 = commento negativo o nullo
# check:	indica l'affidabilità del vettore booleano (ha abbastanza voti?)
class UserProfile(Model):
	user = OneToOneField(User, primary_key=True, default=None)
	simVect = CharField(max_length=5000, default="")
	check = BooleanField(default=0)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		vect = []
		
	def __str__(self):
		return "Profilo di "+str(self.user) 
	
	def getUserId(self):
		return self.user.id
	
	# Aggiorna e restituisce il vettore profilo
	def getVect(self): 
		vect = []
		count = 0
		self.check = 0
		for recensione in models.Recensione.__allRec__():
				found = False
				found, voto = commentsAnalyzer(self, recensione, found)
				if found :
					vect.append(voto) # tengo conto solo dell'ultimo voto
					count = count+1
				else :
					vect.append(0) # il nostro user non ha commentato
		self.simVect = vect.__str__()
		# leggere sopra
		if (count > VOTES_REQUIRED):
			self.check = 1
		return self.simVect
