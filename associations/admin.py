from django.contrib import admin

from associations import models


@admin.register(models.Association)
class AssociationAdmin(admin.ModelAdmin):
    pass

