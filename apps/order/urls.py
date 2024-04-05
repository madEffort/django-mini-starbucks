from django.urls import path, include
from .views import *

app_name = "order"
urlpatterns = [
    path("", ProductView.as_view(), name="product_list"),
    path("product/", ProductView.as_view(), name="product_list"),
    path(
        "product/<int:product_id>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "product/category/<int:category_id>/",
        ProductView.as_view(),
        name="product_category",
    ),
    path("payment/<int:order_id>/", PaymentView.as_view(), name="payment"),
]
