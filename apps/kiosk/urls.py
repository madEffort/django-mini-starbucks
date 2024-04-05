from django.urls import path
from . import views

app_name = "kiosk"
urlpatterns = [
    path("", views.ProductView.as_view(), name="product_list"),
    path("product/", views.ProductView.as_view(), name="product_list"),
    path(
        "product/<int:product_id>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "product/category/<int:category_id>/",
        views.ProductView.as_view(),
        name="product_category",
    ),
    path("cart/<int:order_id>/", views.CartView.as_view(), name="cart"),
    path(
        "cart/<int:order_id>/<int:item_id>/",
        views.RemoveFromCartView.as_view(),
        name="cart_remove_item",
    ),
    path("payment/<int:order_id>/", views.PaymentView.as_view(), name="payment"),
]
