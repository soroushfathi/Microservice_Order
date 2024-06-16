from django.urls import path, include

urlpatterns = [
    path('users/', include(('orderservice.users.urls', 'users'))),
    path('auth/', include(('orderservice.authentication.urls', 'auth'))),
    path('order/', include(('orderservice.order.urls', 'order')))
]
