from datetime import date,datetime 
from django.shortcuts import get_object_or_404 ,redirect, render
from .models import Profile , EmergencyContact
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from django.contrib.auth.decorators import login_required
import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import traceback
from django.shortcuts import redirect
from .models import EmergencyAlert, Profile
from django.utils import timezone
from datetime import timedelta
from .models import EmergencyAlert


def get_emergency_alerts(request):
    alerts = EmergencyAlert.objects.select_related('user').order_by("-created_at")
    data = []

    for alert in alerts:
        data.append({
            "profile_name": f"{alert.user.first_name} {alert.user.last_name}",
            "created_at": alert.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "latitude": alert.latitude,
            "longitude": alert.longitude,
        })

    return JsonResponse({"alerts": data})










@csrf_exempt
def send_safe_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            user = Profile.objects.get(user__id=user_id)
            emergency_contacts = EmergencyContact.objects.filter(profile=user)

            if not emergency_contacts.exists():
                return JsonResponse({
                    "success": False,
                    "error": "Yakın kişi kaydınız bulunamadı. Lütfen en az bir kişi ekleyin."
                })

            for contact in emergency_contacts:
                if not contact.email:
                    continue  # E-posta yoksa atla

                email_subject = "Yakınınız Güvende"
                email_message = render_to_string('account/safe_email.html', {
                    'user': user,
                    'contact': contact
                })

                send_mail(
                    email_subject,
                    'Güvende olduğunuzu bildiren mesaj. Detaylar e-postada.',
                    'noreply@yourdomain.com',
                    [contact.email],
                    fail_silently=False,
                    html_message=email_message,
                )

            return JsonResponse({"success": True})

        except Profile.DoesNotExist:
            return JsonResponse({"success": False, "error": "Kullanıcı bulunamadı"})
        except Exception as e:
            print("E-posta gönderim hatası:", e)
            traceback.print_exc()
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Geçersiz istek türü"})





@csrf_exempt
def send_emergency_email(request):
    if request.method == "POST":
        try:
            # Gelen veriyi alıyoruz
            data = json.loads(request.body)
            user_id = data.get('user_id')
            latitude = data.get('latitude')  # Kullanıcının konumu
            longitude = data.get('longitude')

            # Kullanıcı ve acil durum kişilerini alıyoruz
            
            user = Profile.objects.get(user__id=user_id)
            emergency_contacts = EmergencyContact.objects.filter(profile=user)
            
            for contact in emergency_contacts:
                if not contact.email:
                    continue  # E-posta yoksa atla

                # E-posta içeriğini hazırlıyoruz
                email_subject = "Acil Durum Bildirimi"
                email_message = render_to_string('account/emergency_email.html', {
                    'user': user,
                    'contact': contact,
                    'latitude': latitude,
                    'longitude': longitude
                })

                
                # E-posta gönderimi
                send_mail(
                    email_subject,
                    'Acil durum bildirimi. Detaylar e-postada.',
                    'noreply@yourdomain.com',  # Buraya kendi e-posta adresini yaz
                    [contact.email],
                    fail_silently=False,
                    html_message=email_message,
                )

                    # ✅ Veritabanına acil durum bildirimi kaydı
            EmergencyAlert.objects.create(
                user=user.user,
                address=user.address,
                latitude=latitude,
                longitude=longitude
            )

            
            return JsonResponse({"success": True})
        
              

        except Profile.DoesNotExist:
            return JsonResponse({"success": False, "error": "Kullanıcı bulunamadı"})
        except Exception as e:
            print("E-posta gönderim hatası:", e)
            traceback.print_exc()
            return JsonResponse({"success": False, "error": str(e)})
        
        

    return JsonResponse({"success": False, "error": "Geçersiz istek türü"})









        

  







def destek(request):
    return render(request, "destek.html")





def index(request):
    # Deprem verisi çekme
    url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
    earthquakes = []
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        for item in data.get("result", []):
            try:
                coordinates = item.get("geojson", {}).get("coordinates", [0, 0])
                earthquakes.append({
                    "title": item.get("title", "Bilinmeyen"),
                    "mag": item.get("mag", 0),
                    "date": item.get("date", "Bilinmiyor"),
                    "lat": float(coordinates[1]),
                    "lng": float(coordinates[0]),
                })
            except (TypeError, ValueError, IndexError) as e:
                print("Veri hatası:", e)
    except requests.RequestException as e:
        print("Deprem verisi alınamadı:", e)

    # Acil durum bildirimlerini çekme
    alerts = EmergencyAlert.objects.select_related('user').order_by('-timestamp')[:10]

    return render(request, "pages/index.html", {
        "earthquakes": earthquakes,
        "alerts": alerts
    })


    


def alan(request):
    return render(request,'pages/alan.html')


def destek(request):
    return render(request,'pages/destek.html')








@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profil bulunamadı. Lütfen profilinizi oluşturun.")
        return redirect('update_profile')  # Profil oluşturma sayfasına yönlendirebilirsiniz.
    return render(request, 'pages/profile.html', {'profile': profile})




@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    

    if request.method == "POST":
        profile.first_name = request.POST.get("first_name")
        profile.last_name = request.POST.get("last_name")
        profile.email = request.POST.get("email")
        profile.phone_number = request.POST.get("phone_number")
        profile.birth_date = request.POST.get("birth_date")
        profile.address = request.POST.get("address")
        profile.kan = request.POST.get("kan")
        profile.boy = request.POST.get("boy")
        profile.kilo = request.POST.get("kilo")
        profile.hasta = request.POST.get("hasta")
        profile.ilac = request.POST.get("ilac")
        profile.engel = request.POST.get("engel")
        profile.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect("profile")

    return render(request, "pages/update_profile.html", {'profile': profile})







@login_required
def yakin_ekle(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        surname= request.POST.get("surname")
        email=request.POST.get("email")
        relationship = request.POST.get("relationship")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        
        error = False
        msg = ""
        
        if not name:
            error = True
            msg += "Yakın adı zorunlu bir alandır. "
        elif len(name) < 3:
            error = True
            msg += "Yakın adı en az 3 karakter olmalıdır. "
        
        if not phone_number.isdigit():
            error = True
            msg += "Telefon numarası sadece sayılardan oluşmalıdır. "
        elif len(phone_number) != 11 or not phone_number.startswith("0"):
            error = True
            msg += "Telefon numarası 11 haneli olmalı ve '0' ile başlamalıdır. "

        if error:
            return render(request, "pages/yakin_ekle.html", {"error": True, "msg": msg})
        
        EmergencyContact.objects.create(
            profile=profile,
            name=name,
            surname=surname,
            email=email,
            relationship=relationship,
            phone_number=phone_number,
            address=address
        )
        
        messages.success(request, "Yakın başarıyla eklendi.")
        return redirect("profile")

    return render(request, "pages/yakin_ekle.html")





def delete_emergency_contact(request, contact_id):
    contact = get_object_or_404(EmergencyContact, id=contact_id)  # Burada silinecek yakın kişi seçiliyor
    contact.delete()  # Yakın kişiyi sileriz

    messages.success(request, "Yakın başarıyla silindi.")
    return redirect("profile")  # Profil sayfasına geri yönlendir




def getPathByCategory(request, category):
    
    text = ""
    
    if(category == "dizin"):
        text = "dizin sayfasına giriş"
    elif(category == "dizin-2"):
        text = "dizin -2 sayfasına  giriş"
    else:
        text = "yanlış kategori girişi"
    
    return HttpResponse(text)
