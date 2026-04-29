from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta












class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE )
    first_name = models.CharField("Ad", max_length=50)
    last_name = models.CharField("Soyad", max_length=50,blank=True, null=True)
    birth_date = models.DateField("Doğum Tarihi", null=True, blank=True)
    phone_number = models.CharField("Telefon Numarası", max_length=20)
    address = models.TextField("Adres", null=True, blank=True)
    email = models.EmailField("E-posta", null=True, blank=True)
    kan = models.CharField("Kan Grubu", max_length=20,blank=True, null=True)
    boy = models.CharField("Boy(cm)", max_length=20,blank=True, null=True)
    kilo = models.CharField("Kilo(kg)", max_length=20,blank=True, null=True)
    ilac = models.CharField("Kullandığım İlaçlar(varsa)", max_length=20,blank=True, null=True)
    hasta = models.CharField("Kronik Hastalık(varsa)", max_length=20,blank=True, null=True)
    engel = models.CharField("Engel Drumu(varsa)", max_length=20,blank=True, null=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmergencyContact(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="emergency_contacts")
    name = models.CharField("Yakın Adı", max_length=50,null=True)
    surname = models.CharField("Yakın Adı", max_length=50,blank=True, null=True)
    relationship = models.CharField("Yakınlık Derecesi", max_length=30 , null=True, blank=True)  
    phone_number = models.CharField("Yakın Telefon", max_length=11,null=True, blank=True)
    address = models.TextField("Yakın Adresi",  max_length=100, default="Adres Girilmemiş" ,null=True, blank=True)
    email = models.EmailField("E-posta", null=True, blank=True)



    def __str__(self):
        return f"{self.name} ({self.relationship})"

class EmergencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    address = models.TextField(null=True,blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"