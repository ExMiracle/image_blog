from django.contrib import admin
#from .models import Profile


from .models import Profile, Relationship

class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'from_person'

class PersonAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]

admin.site.register(Profile, PersonAdmin)
# Register your models here.
#admin.site.register(Profile)


