from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from apps.order.models import OrderItem


class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_id = kwargs.get("order_id")
        order_items = OrderItem.objects.filter(order_id=order_id)
        total_price = sum(item.price.price * item.quantity for item in order_items)

        context["order_items"] = order_items
        context["total_price"] = total_price
        context["order_id"] = order_id
        return context


class RemoveFromCartView(View):

    def post(self, request, *args, **kwargs):
        item_id = kwargs.get("item_id")
        order_id = kwargs.get("order_id")
        item = get_object_or_404(OrderItem, id=item_id)
        item.delete()
        return redirect("cart:add_item", order_id=order_id)
