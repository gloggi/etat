
from django.contrib import admin

from suit.admin import SortableModelAdmin

import models

class ParticipantInlineAdmin(admin.TabularInline):
    model = models.Participant
    raw_id_fields = ('member',)
    exclude = ('confirmation',)
    extra = 0


class CampAdmin(admin.ModelAdmin):
    inlines = [ParticipantInlineAdmin]

    class Media:
        css = {"all": ("css/admin.css",)}

class CampTypeAdmin(SortableModelAdmin):
    sortable = 'order'


class ParticipantTypeAdmin(SortableModelAdmin):
    sortable = 'order'


admin.site.register(models.Camp, CampAdmin)
admin.site.register(models.CampType, CampTypeAdmin)
admin.site.register(models.ParticipantType, ParticipantTypeAdmin)