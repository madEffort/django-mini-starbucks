from django.db import models


class ProductCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Product(models.Model):
    product = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(
        default="https://www.naver.com", blank=True
    )  # 임시로 네이버 경로 설정
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product


class Size(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.IntegerField()

    class Meta:
        unique_together = ("product", "size")

    def __str__(self):
        return f"{self.product.product} - {self.size.size} - {self.price}"


class Order(models.Model):
    order_time = models.DateTimeField(auto_now_add=True)
    payment_completed = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class PaymentMethod(models.Model):
    method = models.CharField(max_length=30)

    def __str__(self):
        return self.method


class Payment(models.Model):
    payment_time = models.DateTimeField()
    payment_amount = models.IntegerField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
