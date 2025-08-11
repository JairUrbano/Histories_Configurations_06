from django.shortcuts import render
from django import forms
from .models import (
    DocumentType,
    Patient,
    History,
    PaymentType,
    PredeterminedPrice,
    Appointment,
)

# FORMULARIOS PARA LOS MODELOS

# Formulario para crear/editar tipos de documento
class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name', 'description']

    # Validación personalizada para el campo 'name'
    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Verifica si existe otro tipo con el mismo nombre
        qs = DocumentType.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El tipo de documento ya está registrado.')
        # Valida longitud máxima
        if name and len(name) > 255:
            raise forms.ValidationError('El nombre no debe superar los 255 caracteres.')
        return name

    # Validación para la descripción
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 1000:
            raise forms.ValidationError('La descripción no debe superar los 1000 caracteres.')
        return description

# Formulario para tipos de pago
class PaymentTypeForm(forms.ModelForm):
    class Meta:
        model = PaymentType
        fields = ['code', 'name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = PaymentType.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El tipo de pago ya está registrado.')
        if name and len(name) > 255:
            raise forms.ValidationError('El nombre no debe superar los 255 caracteres.')
        return name

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code and len(code) > 50:
            raise forms.ValidationError('El código no debe superar los 50 caracteres.')
        return code

# Formulario para precios predeterminados
class PredeterminedPriceForm(forms.ModelForm):
    class Meta:
        model = PredeterminedPrice
        fields = ['name', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = PredeterminedPrice.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El precio predeterminado ya está registrado.')
        if name and len(name) > 255:
            raise forms.ValidationError('El nombre no debe superar los 255 caracteres.')
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        # Valida que el precio no sea negativo
        if price is not None and price < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return price

# Formulario para pacientes
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'document_type', 'document_number', 'birth_date']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) > 255:
            raise forms.ValidationError('El nombre no debe superar los 255 caracteres.')
        return name

    def clean_document_number(self):
        document_number = self.cleaned_data.get('document_number')
        if document_number and len(document_number) > 50:
            raise forms.ValidationError('El número de documento no debe superar los 50 caracteres.')
        return document_number

# Formulario para historias clínicas
class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = [
            'testimony', 'private_observation', 'observation',
            'height', 'weight', 'last_weight',
            'menstruation', 'diu_type', 'gestation', 'patient'
        ]

    def clean_diu_type(self):
        diu_type = self.cleaned_data.get('diu_type')
        if diu_type and len(diu_type) > 255:
            raise forms.ValidationError('El tipo de DIU no debe superar los 255 caracteres.')
        return diu_type

# Formulario para citas
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'payment_type',
            'predetermined_price',
            'date',
            'description'
        ]

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 1000:
            raise forms.ValidationError('La descripción no debe superar los 1000 caracteres.')
        return description

    def clean_date(self):
        date = self.cleaned_data.get('date')
        # Para evitar fechas pasadas:
        # from django.utils import timezone
        # if date and date < timezone.now():
        #     raise forms.ValidationError('La fecha no puede estar en el pasado.')
        return date