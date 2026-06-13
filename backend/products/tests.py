import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Product
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify


class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):  # if for set up data change nothing then use setUpTestData
        User = get_user_model()
        cls.user = User.objects.create(username="user1")
        cls.category = Category.objects.create(title="Electronics")

        cls.product1 = Product.objects.create(
            title="product1",
            category=cls.category,
            slug=slugify("Test Product"),
            description="This is a product1.",
            short_description="Short description",
            price=99.99,
            inventory=10,
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"", content_type="image/jpeg"
            ),
            active=True,
        )
        cls.product2 = Product.objects.create(
            title="product2",
            category=cls.category,
            slug=slugify("Test Product2"),
            description="This is a product2.",
            short_description="Short description 2",
            price=99.99,
            inventory=3,
            image=SimpleUploadedFile(
                name="test_image2.jpg", content=b"", content_type="image/jpeg"
            ),
            active=False,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        for product in [cls.product1, cls.product2]:
            if product.image and hasattr(product.image, "path"):
                if os.path.exists(product.image.path):
                    os.remove(product.image.path)

    # def tearDown(self):   for def setUp(self):
    #     # Delete the file from the filesystem
    #     image_path1 = self.product1.image.path
    #     if os.path.exists(image_path1):
    #         os.remove(image_path1)

    #     image_path2 = self.product1.image.path
    #     if os.path.exists(image_path2):
    #         os.remove(image_path2)

    def test_product_model_str(self):
        product = self.product1
        self.assertEqual(str(product), product.title)

    def test_product_detail(self):
        self.assertEqual(self.product1.title, "product1")
        self.assertEqual(self.product1.description, "This is a product1.")

    def test_product_list_url(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

    def test_product_list_url_by_name(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)

    def test_page_title_on_product_list_page(self):
        response = self.client.get(reverse("product_list"))
        self.assertContains(response, self.product1.title)

    def test_product_detail_url(self):
        response = self.client.get(f"/products/{self.product1.id}/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url_by_name(self):
        response = self.client.get(reverse("product_detail", args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_details_on_product_detail_page(self):
        response = self.client.get(f"/products/{self.product1.id}/")
        self.assertContains(response, self.product1.title)
        self.assertContains(response, self.product1.title)

    def test_status_404_if_product_id_not_exist(self):
        response = self.client.get(reverse("product_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_product_not_show_in_products_list(self):
        response = self.client.get(reverse("product_list"))
        self.assertContains(response, self.product1.title)
        self.assertNotContains(response, self.product2.title)
