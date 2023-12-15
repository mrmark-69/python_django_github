from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.forms import ModelForm
from .models import Product, Order, ProductImage


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "discount", "preview"]

    images = MultipleFileField(required=False)


class ProductUpdateForm(ProductForm):
    images_to_delete = forms.ModelMultipleChoiceField(
        queryset=ProductImage.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label= "Already existing images:",
        help_text="mark to delete.",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('pk')
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['images_to_delete'].queryset = ProductImage.objects.filter(product_id=product_id)


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].empty_label = 'select customer'
        self.fields["user"].label = "Customer"
        self.fields["products"].queryset = Product.objects.filter(archived=False)

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
            raise ValidationError("Fill in the delivery address.")
        return delivery


class ConfirmForm(forms.Form):
    confirm_action = forms.BooleanField(required=False)

    def clean(self):
        if self.cleaned_data['confirm_action'] is False:
            raise ValidationError('You must confirm this form')
        return super(ConfirmForm, self).clean()


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()