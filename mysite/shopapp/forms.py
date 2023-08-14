from django import forms
from django.core.exceptions import ValidationError

# from django.core import validators
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "discount"]


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].empty_label = 'select customer'
        self.fields["user"].label = "Customer"

    class Meta:
        model = Order
        fields = ["user", "products", "delivery_address", "promocode", ]
        widgets = {
            'delivery_address': forms.Textarea(attrs={"cols": "40", "rows": "5"}),
        }

    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              )

    def clean_delivery_address(self):
        delivery = self.cleaned_data['delivery_address']
        if len(delivery) == 0:
            raise ValidationError("Заполните адрес доставки.")
        return delivery
