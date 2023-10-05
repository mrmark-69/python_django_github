import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product


class ShopIndexTestCase(TestCase):

    def test_index(self):
        response = self.client.get(reverse('shopapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('THIS TEXT WILL BE HTML-ESCAPED, AND WILL APPEAR IN ALL UPPERCASE.', response.content.decode())


class ProductCreateTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='admin', password='admin')
        permission = Permission.objects.get(codename='add_product')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_product_create(self):
        response = self.client.post(reverse('shopapp:product_create'),
                                    {
                                        "name": "Table_test",
                                        "price": "12.99",
                                        "description": "A test_table",
                                        "discount": "7",
                                    }
                                    )
        self.assertRedirects(response, reverse('shopapp:products_list'))


class ProductsTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.product = Product.objects.create(name="Tablet")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()
        super().tearDownClass()

    def test_products_list(self):
        response = self.client.get(reverse('shopapp:products_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Products list', response.content.decode())

    def test_product_detail_and_check_content(self):
        response = self.client.get(reverse('shopapp:product_details', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Product #', response.content.decode())
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        'groups-fixture.json'
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))

        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=[p.pk for p in response.context["products"]],
            transform=lambda p: p.pk
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.credentials = dict(username='Test_user', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')
