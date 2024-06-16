from django.urls import path, include

urlpatterns = [
    path('order/', include(('orderservice.order.urls', 'order')))
]
