from django.db import models


class ProductCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class ProductSize(models.Model):
    size = models.CharField(max_length=100)

    def __str__(self):
        return self.size


class Product(models.Model):
    product = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(
        default="https://image.istarbucks.co.kr/upload/store/skuimg/2021/04/[9200000002487]_20210426091745467.jpg",
        blank=True,
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product.product} - {self.size.size} - {self.price}"


class Order(models.Model):
    order_time = models.DateTimeField(auto_now_add=True)
    payment_completed = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class PaymentMethod(models.Model):
    method = models.CharField(max_length=100)

    def __str__(self):
        return self.method


class Payment(models.Model):
    payment_time = models.DateTimeField()
    payment_amount = models.IntegerField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
