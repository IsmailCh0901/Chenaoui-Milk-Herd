from django.apps import AppConfig

class HerdappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'herdapp'

    def ready(self):
        from django.contrib import admin
        admin.site.site_header = "ELEVAGE LAITIER CHENAOUI — Admin"
        admin.site.site_title = "ELEVAGE LAITIER CHENAOUI"
        admin.site.index_title = "Dashboard"
