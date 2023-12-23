from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductViewSet, OrdersViewSet, LatestProductsFeed

app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrdersViewSet)

urlpatterns = [
    path("", views.ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", views.GroupsListView.as_view(), name="groups_list"),

    path("products/", views.ProductsListView.as_view(), name="products_list"),
    path("products/export/", views.ProductDataExportView.as_view(), name="products_export"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", views.ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", views.ProductArchiveView.as_view(), name="product_archive"),
    path("products/latest/feed/", LatestProductsFeed(), name="products-feed"),

    path("orders/", views.OrdersListView.as_view(), name="orders_list"),
    path("user/<int:user_id>/orders/", views.UserOrdersListView.as_view(), name="user_orders_list"),
    path('user/<int:user_id>/orders/export/', views.UserOrdersExportView.as_view(), name='export_user_orders'),
    path("orders/export/", views.OrdersExportView.as_view(), name="orders_export"),
    path("orders/<int:pk>", views.OrderDetailView.as_view(), name="order_details"),
    path("orders/create/", views.OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", views.OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order_delete"),
]
