from django.urls import path
from .views import *

app_name = "cart"
urlpatterns = [
    path("<int:order_id>/", CartView.as_view(), name="add_item"),
    path(
        "<int:order_id>/<int:item_id>/",
        RemoveFromCartView.as_view(),
        name="remove_item",
    ),
]
