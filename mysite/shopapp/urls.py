from django.urls import path

from . import views

app_name = 'shopapp'

urlpatterns = [
    path("", views.ShopIndexView.as_view(), name="index"),
    path("groups/", views.GroupsListView.as_view(), name="groups_list"),
    path("products/", views.ProductsListView.as_view(), name="products_list"),
    path("products/export/", views.ProductDataExportView.as_view(), name="products_export"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", views.ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", views.ProductArchiveView.as_view(), name="product_archive"),
    path("orders/", views.OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", views.OrdersExportView.as_view(), name="orders_export"),
    path("orders/<int:pk>", views.OrderDetailView.as_view(), name="order_details"),
    path("orders/create/", views.OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", views.OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order_delete"),
]
