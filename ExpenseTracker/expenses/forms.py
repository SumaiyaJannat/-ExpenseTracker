from django import forms
from django.core.exceptions import ValidationError
from .models import Expense, Budget,Category

class AddMoneyForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    title = forms.CharField(max_length=100)
    quantity = forms.DecimalField(max_digits=10, decimal_places=2)
    Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise ValidationError('Amount must be greater than zero.')
        return quantity
    

class AddBudgetForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    budget_limit = forms.DecimalField(max_digits=10, decimal_places=2)
    
    def clean_budget_limit(self):
        budget_limit = self.cleaned_data.get('budget_limit')
        if budget_limit <= 0:
            raise ValidationError('Amount must be greater than zero.')
        return budget_limit
    

class EditExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'quantity', 'Date', 'category']
        widgets = {
            'category': forms.Select(),
        }


class EditBudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['budget_limit', 'category']
        widgets = {
            'category': forms.Select(),
        }

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_active']

