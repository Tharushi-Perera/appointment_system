from django import forms
from .models import Appointment, Service, ServiceCategory, ServiceSubCategory
from django.forms import ModelForm


class AppointmentForm(ModelForm):
    category = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.all(),
        required=True,
        label="Service Category",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_category'
        })
    )

    subcategory = forms.ModelChoiceField(
        queryset=ServiceSubCategory.objects.none(),
        required=True,
        label="Service Subcategory",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_subcategory'
        })
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        required=True,
        label="Service",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_service'
        })
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Appointment
        fields = ['category', 'subcategory', 'service', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If the form is bound (submitted), update the querysets
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = ServiceSubCategory.objects.filter(
                    category_id=category_id
                ).order_by('display_order')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and hasattr(self.instance, 'service'):
            # If editing an existing appointment
            self.fields['subcategory'].queryset = self.instance.service.subcategory.category.subcategories.all()
            self.fields['service'].queryset = self.instance.service.subcategory.services.all()

        # Set initial category if subcategory is provided
        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                subcategory = ServiceSubCategory.objects.get(id=subcategory_id)
                self.fields['category'].initial = subcategory.category
                self.fields['subcategory'].queryset = ServiceSubCategory.objects.filter(
                    category=subcategory.category
                ).order_by('display_order')
                self.fields['service'].queryset = Service.objects.filter(
                    subcategory_id=subcategory_id
                ).order_by('name')
            except (ValueError, TypeError, ServiceSubCategory.DoesNotExist):
                pass
        elif self.instance.pk and hasattr(self.instance, 'service'):
            # If editing an existing appointment
            self.fields['category'].initial = self.instance.service.subcategory.category
            self.fields['subcategory'].initial = self.instance.service.subcategory
            self.fields['service'].queryset = self.instance.service.subcategory.services.all()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        service = cleaned_data.get('service')

        # Validate that subcategory belongs to selected category
        if category and subcategory:
            if subcategory.category != category:
                raise forms.ValidationError(
                    "Selected subcategory doesn't belong to the selected category"
                )

        # Validate that service belongs to selected subcategory
        if subcategory and service:
            if service.subcategory != subcategory:
                raise forms.ValidationError(
                    "Selected service doesn't belong to the selected subcategory"
                )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set empty labels
        self.fields['category'].empty_label = "Select a category"
        self.fields['subcategory'].empty_label = "Select a subcategory"
        self.fields['service'].empty_label = "Select a service"

        # Order categories by display_order
        self.fields['category'].queryset = ServiceCategory.objects.all().order_by('display_order')
