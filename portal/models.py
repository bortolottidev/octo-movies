from django.db.models import Model, BooleanField, OneToOneField, CharField
from django.contrib.auth.models import User
from recensioni.utility import commentsAnalyzer
from recensioni import models

# Estremamente basso a causa del mio database fittizio
VOTES_REQUIRED = 2

# Profilo utente, per la profilizzazione dei suoi commenti rilasciati
class UserProfile(Model):
	user = OneToOneField(User, primary_key=True, default=None)
	# L'utente è profilizzato con un vettore like/dislike dei commenti postati
	simVect = CharField(max_length=5000, default="")
	check = BooleanField(default=0)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		vect = []
		
	def __str__(self):
		return str(self.user)+" profilo" 
	
	def getUserId(self):
		return self.user.id
	
	# aggiorna e restituisce il vettore profilo
	def getVect(self): 
		vect = []
		count = 0
		self.check = 0
		for recensione in models.Recensione.__allRec__():
				found = False
				found, voto = commentsAnalyzer(self, recensione, found)
				if found :
					#print("Appendo "+str(voto)+" in "+str(recensione))
					vect.append(voto) # tengo conto solo dell'ultimo voto
					count = count+1
				else :
					#print("Non trovato niente su "+str(recensione))
					vect.append(0) # il nostro user non ha commentato
		self.simVect = vect.__str__()
		# Il profilo di un utente viene considerato valido se ha dato almeno n voti
		if (count > VOTES_REQUIRED):
			self.check = 1
		
		#print(str(self.simVect)+" di "+str(self.user))
		return self.simVect
