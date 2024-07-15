from django.contrib import admin

from apps.connection.models import UserConnection, ConnectionRequest

admin.site.register(UserConnection)
admin.site.register(ConnectionRequest)
