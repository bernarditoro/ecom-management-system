from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="product-categories-img")

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self) -> str:
        return self.name


class ProductColour(models.Model):
    colour = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Product Colour"
        verbose_name_plural = "Product Colours"

    def __str__(self) -> str:
        return self.colour


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="product")
    stock = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="product-images")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    colours = models.ManyToManyField(ProductColour, related_name="products")
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    images = models.ImageField(upload_to="product-images")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self) -> str:
        return f"{self.product}'s image"
