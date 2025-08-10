from django.db import models
from django.utils import timezone

# Modelo para el tipo de documento
class DocumentType(models.Model):
    name = models.CharField(max_length=255)  # Nombre del tipo de documento
    description = models.TextField(blank=True, null=True)  # Descripción adicional

    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)      # Fecha de última actualización
    deleted_at = models.DateTimeField(blank=True, null=True)  # Fecha de borrado lógico

    # Método para realizar borrado lógico (no elimina el registro de la BD, solo marca la fecha de borrado)
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    # Método para restaurar el registro (quita la marca de borrado)
    def restore(self):
        self.deleted_at = None
        self.save()

    # Cómo se muestra el objeto como string
    def _str_(self):
        return self.name

    # Indica el nombre de la tabla en la base de datos
    class Meta:
        db_table = "document_types"

# Modelo para los pacientes
class Patient(models.Model):
    name = models.CharField(max_length=255)  # Nombre del paciente
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )  # Relación con tipo de documento (puede quedar en null si se elimina el tipo de documento)
    document_number = models.CharField(max_length=50, blank=True, null=True)  # Número de documento
    birth_date = models.DateField(blank=True, null=True)  # Fecha de nacimiento

    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)      # Fecha de última actualización

    def _str_(self):
        return self.name

    class Meta:
        db_table = "patients"


# Modelo para la historia clínica de un paciente
class History(models.Model):
    testimony = models.TextField(blank=True, null=True)  # Testimonio del paciente
    private_observation = models.TextField(blank=True, null=True)  # Observaciones privadas
    observation = models.TextField(blank=True, null=True)  # Observaciones generales
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Altura en metros
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Peso actual
    last_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Último peso registrado
    menstruation = models.BooleanField(default=False)  # Si la paciente tiene menstruación
    diu_type = models.CharField(max_length=255, blank=True, null=True)  # Tipo de DIU
    gestation = models.BooleanField(default=False)  # Si la paciente está en gestación

    patient = models.ForeignKey(
        Patient,
        related_name="histories",
        on_delete=models.CASCADE
    )  # Relación con el paciente (si se elimina el paciente, se eliminan sus historias)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)  # Borrado lógico

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def _str_(self):
        return f"History for patient {self.patient_id}"

    class Meta:
        db_table = "histories"


# Modelo de tipos de pago
class PaymentType(models.Model):
    code = models.CharField(max_length=50)  # Código interno del tipo de pago
    name = models.CharField(max_length=255) # Nombre del tipo de pago

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)  # Borrado lógico

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def _str_(self):
        return self.name

    class Meta:
        db_table = "payment_types"


# Modelo para precios predeterminados
class PredeterminedPrice(models.Model):
    name = models.CharField(max_length=255)  # Nombre del precio predeterminado
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Valor del precio

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.name} - {self.price}"

    class Meta:
        db_table = "predetermined_prices"


# Modelo para las citas médicas
class Appointment(models.Model):
    payment_type = models.ForeignKey(
        PaymentType,
        related_name="appointments",
        on_delete=models.CASCADE
    )  # Relación con tipo de pago
    predetermined_price = models.ForeignKey(
        PredeterminedPrice,
        related_name="appointments",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )  # Relación con precio predeterminado

    date = models.DateTimeField()  # Fecha y hora de la cita
    description = models.TextField(blank=True, null=True)  # Descripción de la cita

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "appointments"