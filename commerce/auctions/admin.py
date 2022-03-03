from django.contrib import admin
from .models import listing, bids, comments, User, watchlist
# Register your models here.
admin.site.register(listing)
admin.site.register(comments)
admin.site.register(bids)
admin.site.register(User)
admin.site.register(watchlist)
