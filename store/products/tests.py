from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class IndexViewTest(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Adidas')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTest(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_products_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products[:1])
        )

    def test_products_list_categories(self):
        category = Category.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Catalog')
        self.assertTemplateUsed(response, 'products/products.html')
