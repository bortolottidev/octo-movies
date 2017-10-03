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
	list_display = ('titolo', 'autore', 'pub_date', 'published_recently', 
				 'num_voti')
	list_filter =  ['pub_date']
	search_fields = ['titolo']
	
class CommentoAdmin(admin.ModelAdmin):
	fields = ['recensione', 'autore', 'voto', 'testo']

class TagAdmin(admin.ModelAdmin):
	fields = ['nome', 'recensione']

admin.site.register(Recensione, RecensioneAdmin)
admin.site.register(Commento, CommentoAdmin)
admin.site.register(Tag, TagAdmin)
