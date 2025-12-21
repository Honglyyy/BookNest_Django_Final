from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Category(models.Model):
    categoryName = models.CharField(max_length=200, null=True)
    categoryImage = models.ImageField(upload_to='images/Categories/', null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.categoryName}'


class Genre(models.Model):
    genreName = models.CharField(max_length=200, null=True)
    genreImage = models.ImageField(upload_to='images/Genre/', null=True, blank=True)
    categoryId = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='genres'
    )

    def __str__(self):
        return f'{self.id} - Genre: {self.genreName} || CategoryID: {self.categoryId}'

class Product(models.Model):
    productName = models.CharField(max_length=200, null=True)
    genreID = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    originalPrice = models.FloatField(null=True)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)
    productDescription =  RichTextUploadingField(null=True)
    productImage = models.ImageField(upload_to='images/Products/',null=True,blank=True)
    addedDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id} - {self.productName} - {self.addedDate}'

class ProductDetail(models.Model):
    productDetailName = models.CharField(max_length=200, null=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    Reviews = RichTextUploadingField(null=True)
    addedDate = models.DateTimeField (auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.id} - {self.productID.productName} - {self.productDetailName}'

class ProductDetailImage(models.Model):
    productDetailImageName = models.CharField(max_length=200, null=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    productDetailImage = models.ImageField(upload_to='images/productDetail/',null=True,blank=True)
    addedDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.id} - {self.productID.productName} - {self.productDetailImageName}'

class Blog(models.Model):
    blogID = models.CharField(max_length=200, null=True)
    blogTitle = models.CharField(max_length=200, null=True)
    blogDescription = RichTextUploadingField(null=True)
    blogImage = models.ImageField(upload_to='images/Blogs/',null=True,blank=True)
    addedDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.id} - {self.blogID} - {self.blogTitle}'

class BillingDetail(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    town = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    qr_code_image = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    total = models.FloatField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"