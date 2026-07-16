from django.contrib import admin

from board.models import Hold, Layout, LayoutHold, Route, RouteHold

admin.site.register(Layout)
admin.site.register(LayoutHold)
admin.site.register(Route)
admin.site.register(RouteHold)
admin.site.register(Hold)
