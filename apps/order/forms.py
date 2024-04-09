from django import forms

class ProductForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    size_id = forms.ChoiceField(choices=[], widget=forms.Select(attrs={
        'class': 'px-3 py-2 border border-gray-300 rounded-lg w-full dark:bg-gray-700 dark:border-gray-600 dark:text-white'
    }))
    quantity = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={
        'class': 'px-3 py-2 border border-gray-300 rounded-lg w-full dark:bg-gray-700 dark:border-gray-600 dark:text-white'
    }))
    
    def __init__(self, *args, **kwargs):
        size_choices = kwargs.pop('size_choices', [])
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['size_id'].choices = size_choices

class PaymentForm(forms.Form):
    payment_amount = forms.IntegerField(widget=forms.HiddenInput())
    payment_method = forms.ChoiceField(choices=[], widget=forms.Select(attrs={
        'class': 'w-full'
    }))
    
    def __init__(self, *args, **kwargs):
        method_choices = kwargs.pop('method_choices', [])
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].choices = method_choices