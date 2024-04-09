from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

from django.views.generic import ListView, View, TemplateView, FormView
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
from django.contrib import messages
from django.shortcuts import redirect
from apps.order.forms import ProductForm, PaymentForm


class ProductView(ListView):
    model = Product
    template_name = "order/product_list.html"
    context_object_name = "product_list"
    paginate_by = 18

    def get_queryset(self):
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


class ProductDetailView(FormView):

    form_class = ProductForm
    template_name = "order/product_detail.html"

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        product_id = self.kwargs.get("product_id")
        size_choices = [
            (product.size.id, str(product.size.size))
            for product in Price.objects.filter(product_id=product_id)
        ]
        kwargs["size_choices"] = size_choices
        kwargs["initial"] = {"product_id": product_id}
        return kwargs

    def form_valid(self, form):
        product_id = form.cleaned_data.get("product_id")
        size_id = form.cleaned_data.get("size_id")
        quantity = form.cleaned_data.get("quantity")
        order_id = self.request.session.get("order_id")

        if order_id:
            order = Order.objects.filter(id=order_id, payment_completed=False).first()

        if not order_id or not order:
            order = Order.objects.create()
            self.request.session["order_id"] = order.id

        OrderItem.objects.create(
            order=order,
            product=Product.objects.get(pk=product_id),
            price=Price.objects.filter(product__id=product_id, size_id=size_id).get(),
            quantity=quantity,
        )

        return redirect("cart:add_item", order_id=order.id)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        context["product"] = product
        return context


class CartView(TemplateView):
    template_name = "order/cart.html"

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
        return redirect("cart:remove_item", order_id=order_id)


class PaymentView(FormView):

    form_class = PaymentForm
    template_name = "order/payment.html"

    def get_form_kwargs(self):
        kwargs = super(PaymentView, self).get_form_kwargs()
        order_id = kwargs.get("order_id")
        order_items = OrderItem.objects.filter(order_id=order_id)
        payment_amount = sum(item.price.price * item.quantity for item in order_items)
        method_choices = [
            (method.id, str(method.method)) for method in PaymentMethod.objects.all()
        ]
        kwargs["method_choices"] = method_choices
        kwargs["initial"] = {"payment_amount": payment_amount}
        return kwargs

    def form_valid(self, form):
        order_id = self.kwargs.get("order_id")
        payment_method_id = form.cleaned_data.get("payment_method")
        payment_amount = form.cleaned_data.get("payment_amount")
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

        messages.success(self.request, "결제가 완료되었습니다.")
        return redirect("order:product_list")

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        order_id = self.kwargs.get("order_id")
        order_items = OrderItem.objects.filter(order_id=order_id)
        context["order_items"] = order_items
        context["order_id"] = order_id
        return context
