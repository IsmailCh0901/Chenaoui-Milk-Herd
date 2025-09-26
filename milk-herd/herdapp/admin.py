from django.contrib import admin
from .models import Animal, MilkRecord

class MilkRecordInline(admin.TabularInline):
    model = MilkRecord
    extra = 1
    fields = ('date', 'liters', 'notes')
    ordering = ('-date',)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("ear_tag","name","sex","breed","date_of_birth","sire","dam","is_alive")
    search_fields = ("ear_tag","name","breed")
    list_filter = ("sex","breed","is_alive")
    autocomplete_fields = ("sire","dam")
    inlines = [MilkRecordInline]

@admin.register(MilkRecord)
class MilkRecordAdmin(admin.ModelAdmin):
    list_display = ("animal","date","liters","notes")
    list_filter = ("date",)
    search_fields = ("animal__ear_tag","animal__name","notes")
    autocomplete_fields = ("animal",)
