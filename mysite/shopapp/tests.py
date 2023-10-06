import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from mysite import settings
from shopapp.models import Product, Order


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

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
        'groups-fixture.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='admin_plus', password='admin')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="04778, 30527 Schultz Ford, Lake Rosendochester, South Carolina",
            promocode="promoCode_12_3",
            user=self.user
        )
        self.order.products.set([29, 30, 31, 32])
        super().setUp()

    def tearDown(self):
        self.order.delete()
        super().tearDown()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', args=[self.order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.order.delivery_address, response.content.decode())
        self.assertIn(self.order.promocode, response.content.decode())

        context_order = response.context['order']
        self.assertEqual(context_order.pk, self.order.pk)
