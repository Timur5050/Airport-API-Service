from flights.models import (
    Airport,
    Crew,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket,
)

from django.contrib import admin


admin.site.register(Airport)
admin.site.register(Crew)
admin.site.register(Route)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
