from django.contrib import admin

from accounts.models import Profile
from accounts.models import User
from accounts.models import Seller
from accounts.models import Address
from accounts.models import Message
# Register your models here.
admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Message)
