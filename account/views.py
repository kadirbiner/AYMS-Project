from django.shortcuts import redirect, render  # type: ignore
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.core.mail import BadHeaderError





def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        

        # Türkçe harflerle birlikte sadece harflerden oluşan ve en az 3 karakter uzunluğunda kontrol
        if not re.fullmatch(r'[a-zA-ZçÇğĞıİöÖşŞüÜ]{3,}', username):
            return render(request, "account/register.html", {
                "error": "Kullanıcı adı en az 3 harf olmalı ve sadece harf içermelidir.",
                "username": username,
                "lastname": lastname,
                
            })




          

        if not re.fullmatch(r"0\d{10}", phone):
            return render(request, "account/register.html", {
                "error": "Telefon numarası 11 haneli olmalı ve 0 ile başlamalıdır.",
                "username": username,
                "lastname": lastname,
                "email": email,
                "phone": phone
            })

        
        
        
    

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {
                    "error": "Kullanıcı adı kullanılıyor.",
                    "username": username,
                    "lastname": lastname,
                    "email": email
                })
            elif User.objects.filter(email=email).exists():
                return render(request, "account/register.html", {
                    "error": "Bu e-mail daha önce kayıt edilmiş.",
                    "username": username,
                    "lastname": lastname,
                    "email": email
                })
                
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.last_name = lastname
                user.is_active = False  # Hesap doğrulanana kadar giriş yapılamasın
                user.save()

                # Token ve uid oluştur
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Doğrulama linki oluştur (tam URL)
                relative_link = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
                link = request.build_absolute_uri(relative_link)

                # HTML e-posta içeriği
                email_subject = "Hesabınızı Doğrulayın"
                email_message = render_to_string('account/email_verification.html', {
                    'user': user,
                    'link': link
                })

                # E-posta gönder
                try:
                    send_mail(
                        email_subject,
                        '',  # plain-text body boş
                        'a.kadirbiner@gmail.com',  # Gerçek gönderici adresin olmalı (örn: gmail)
                        [email],
                        fail_silently=False,
                        html_message=email_message,  # HTML içerik
                    )
                except (BadHeaderError, Exception):
                    user.delete()
                    return render(request, "account/register.html", {
                        "error": "Doğrulama e-postası gönderilemedi. E-posta ayarlarınızı kontrol edip tekrar deneyin.",
                        "username": username,
                        "lastname": lastname,
                        "email": email,
                        "phone": phone,
                    })

                messages.success(request, "Kayıt başarılı. Lütfen e-postanızı doğrulayın.")
                return redirect("email_verification_info")
        else:
            return render(request, "account/register.html", {"error": "Şifreler eşleşmiyor."})

    return render(request, "account/register.html")






def email_verification_info(request):
    return render(request, "account/email_verification_info.html")













def verify_email(request, uidb64, token):
    try:
        # Kullanıcı ID'sini çöz
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_user_model().objects.get(pk=uid)
        
        # Token doğrulama
        if default_token_generator.check_token(user, token):
            user.is_active = True  # Kullanıcıyı aktif yap
            user.save()
            messages.success(request, "E-posta doğrulaması başarılı. Giriş yapabilirsiniz.")
            return redirect("user_login")
        else:
            messages.error(request, "Geçersiz doğrulama bağlantısı.")
            return redirect("user_login")
    except Exception as e:
        messages.error(request, f"Doğrulama hatası: {str(e)}")
        return redirect("user_login")


# Kullanıcı kaydı





def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.add_message(request,messages.SUCCESS ,"Giriş Başarılı")
            return redirect("index")
        else:
            return render(request,"account/login.html",{"error":"kullanıcı adı veya şifre yanlış"})
    else:
        return render(request,"account/login.html")
    
    
    



def user_logout(request):
    messages.add_message(request,messages.SUCCESS ,"Çıkış  Başarılı")
    logout(request)
    return redirect("index")