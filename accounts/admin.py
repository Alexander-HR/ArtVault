from django.contrib import admin

from accounts.models import (
    Profile,
    User,
    Seller,
    Address,
    Notification,
    Message,
)

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Notification)
admin.site.register(Message)