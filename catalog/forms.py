from django import forms

from catalog.models import Product, Version


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})


class ProductForm(StyleFormsMixin, forms.ModelForm):

    words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name_products', 'description_products', 'image', 'price', 'category',)

    def clean_name_products(self):
        cleaned_data = self.cleaned_data['name_products']

        for word in self.words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Название не должно содержать слово' + word)
        return cleaned_data

    def clean_description_products(self):
        cleaned_data = self.cleaned_data['description_products']

        for word in self.words:
            if word.lower() in cleaned_data.lower():
                raise forms.ValidationError('Описание не должно содержать слово' + word)
        return cleaned_data


class VersionForm(StyleFormsMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
