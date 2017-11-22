from django.contrib import admin
from .models import Recensione, Commento, Tag

class TagRecensioneInline(admin.StackedInline):
	model = Tag.recensione.through
	extra = 2
	classes = ('collapse', )

class CommentoInline(admin.StackedInline):
	model = Commento
	extra = 4
	classes = ('collapse', )

# Customizziamo, non voglio che il rank sia influenzabile dagli admin
class RecensioneAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,				{'fields': ['titolo', 'autore', 'testo', 'voto']}),
		('Info aggiuntive',	{'fields': ['genere'], 'classes': ['collapse']})
	]
	inlines = [CommentoInline, TagRecensioneInline]
	field_to_disp = Recensione.campi()
	field_to_disp.remove('testo')
	list_display = field_to_disp
	search_fields = ['titolo']
	list_filter = ['pub_date']
	
class CommentoAdmin(admin.ModelAdmin):
	fields = ['recensione', 'autore', 'voto', 'testo']
	list_display = ['titoloRecens', 'autore', 'votoRecens', '__str__']
	list_filter = ['autore']
	
	def votoRecens(self,obj):
		if obj.voto:
			return "Positivo"
		return "Negativo o Nullo"
	votoRecens.short_description = 'Voto'
	
	def titoloRecens(self,obj) :
		return obj.recensione.titolo
	titoloRecens.admin_order_field = 'recensione__titolo'
	titoloRecens.short_description = 'Titolo'

class TagAdmin(admin.ModelAdmin):
	fields = ['nome', 'recensione']
	list_display = ['__str__', 'getRecensioni']
	
	def getRecensioni(self,obj):
		return [x.__str__() for x in obj.recensione.all()]
	getRecensioni.short_description = 'Recensioni associate'

admin.site.register(Recensione, RecensioneAdmin)
admin.site.register(Commento, CommentoAdmin)
admin.site.register(Tag, TagAdmin)
