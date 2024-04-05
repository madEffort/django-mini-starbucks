from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

from django.views.generic import ListView, View, TemplateView
from .models import (
    Product,
    ProductCategory,
    Price,
    Order,
    OrderItem,
    PaymentMethod,
    Payment,
)
from django.utils import timezone


class ProductView(ListView):
    model = Product
    template_name = "kiosk/product_list.html"
    context_object_name = "product_list"
    paginate_by = 18

    def get_queryset(self):
        """
        URL의 category_id를 기반으로 Product 쿼리셋을 필터링합니다.
        """
        category_id = self.kwargs.get("category_id")
        if category_id:
            return Product.objects.filter(category__id=category_id)
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = ProductCategory.objects.all()
        context["category"] = category
        return context


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        price = get_list_or_404(Price, product=product)
        context = {"product": product, "price": price}
        return render(request, "kiosk/product_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        size_id = request.POST.get("size_id")
        quantity = request.POST.get("quantity")
        order_id = request.session.get("order_id")

        if order_id:
            order = Order.objects.filter(id=order_id, payment_completed=False).first()

        # 주문이 없거나 세션에 주문 ID가 없는 경우 새로운 주문 생성
        if not order_id or not order:
            order = Order.objects.create()
            # 새로운 주문의 ID를 세션에 저장
            request.session["order_id"] = order.id
            order_id = order.id

        OrderItem.objects.create(
            order=order,
            product=Product.objects.filter(pk=product_id).get(),
            price=Price.objects.filter(product__id=product_id, size_id=size_id).get(),
            quantity=quantity,
        )
        return redirect("kiosk:cart", order_id)


class CartView(TemplateView):
    template_name = "kiosk/cart.html"

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
        return redirect("kiosk:cart", order_id=order_id)


class PaymentView(View):

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        order_items = OrderItem.objects.filter(order_id=order_id)
        payment_amount = sum(item.price.price * item.quantity for item in order_items)
        payment_method = PaymentMethod.objects.all()
        context = {"payment_method": payment_method, "payment_amount": payment_amount}
        return render(request, "kiosk/payment.html", context=context)

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        payment_method_id = request.POST.get("payment_method")
        payment_amount = int(request.POST.get("payment_amount"))
        payment_method = PaymentMethod.objects.get(id=payment_method_id)
        order = Order.objects.get(id=order_id)
        Payment.objects.create(
            payment_time=timezone.now(),
            payment_amount=payment_amount,
            payment_method=payment_method,
            order=order,
        )
        order.payment_completed = True
        order.save()

        return redirect("kiosk:product_list")
