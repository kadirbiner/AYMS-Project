//deprem verileri
document.addEventListener("DOMContentLoaded", function () {
  const liveMap = L.map("live-earthquake-map").setView([39.0, 35.0], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap katkıcıları",
  }).addTo(liveMap);

  let earthquakeData = [];

  try {
    const rawData = `{{ earthquakes|default:"[]"|safe|escapejs }}`;
    earthquakeData = JSON.parse(rawData);
  } catch (e) {
    console.warn("Deprem verisi alınamadı:", e);
  }

  earthquakeData.forEach((quake) => {
    const lat = parseFloat(quake.lat);
    const lng = parseFloat(quake.lng);
    const mag = parseFloat(quake.mag);

    let color = "green";
    if (mag >= 4 && mag < 5) color = "orange";
    else if (mag >= 5) color = "red";

    const marker = L.circleMarker([lat, lng], {
      radius: 5 + mag,
      color: color,
      fillColor: color,
      fillOpacity: 0.6,
    }).addTo(liveMap);

    marker.bindPopup(`
      <strong>${quake.title}</strong><br />
      Şiddet: ${mag}<br />
      Zaman: ${quake.date}
    `);
  });

  document.querySelectorAll(".show-on-map").forEach((button) => {
    button.addEventListener("click", function () {
      const lat = parseFloat(button.getAttribute("data-lat"));
      const lng = parseFloat(button.getAttribute("data-lng"));
      const title = button.closest("li").querySelector("strong").textContent;

      liveMap.setView([lat, lng], 12);

      L.marker([lat, lng])
        .addTo(liveMap)
        .bindPopup(`<strong>${title}</strong><br />Haritada gösterildi.`)
        .openPopup();
    });
  });

  // Konum gönderme işlemi
  function getCSRFToken() {
    return document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
  }
});

//uyarı süresi
setTimeout(function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    alert.classList.add("fade-out");
    setTimeout(() => alert.remove(), 1000); // animasyon süresi kadar bekle
  });
}, 1500); // 3 saniye sonra başla

//slider kodları
var swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  spaceBetween: 20,
  loop: true,
  autoplay: {
    delay: 3000, // 3 saniyede bir geçiş
    disableOnInteraction: false,
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    768: {
      slidesPerView: 2,
    },
    992: {
      slidesPerView: 3,
    },
  },
});

// Güvendeyim
function sendSafe() {
  const userId = document
    .getElementById("safe-button")
    .getAttribute("data-user-id");

  fetch("/send-safe-email/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
    },
    body: JSON.stringify({
      user_id: userId,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Yakınlarınıza güvende olduğunuz bildirildi.");
      } else {
        // Sunucudan gelen özel hata mesajını göster
        alert(data.error || "Bir hata oluştu, lütfen tekrar deneyin.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Sunucuya bağlanırken bir hata oluştu.");
    });
}

//yüklenme animasyonu
function sendSafe() {
  const userId = document
    .getElementById("safe-button")
    .getAttribute("data-user-id");

  const spinner = document.getElementById("loading-spinner");
  spinner.style.display = "block"; // Spinner'ı göster

  fetch("/send-safe-email/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
    },
    body: JSON.stringify({ user_id: userId }),
  })
    .then((response) => response.json())
    .then((data) => {
      spinner.style.display = "none"; // Spinner'ı gizle
      if (data.success) {
        alert("Yakınlarınıza güvenli olduğunuz bildirildi.");
      } else {
        alert(data.error || "Bir hata oluştu, lütfen tekrar deneyin.");
      }
    })
    .catch((error) => {
      spinner.style.display = "none"; // Spinner'ı gizle
      console.error("Error:", error);
      alert("Sunucu hatası oluştu, lütfen tekrar deneyin.");
    });
}

// Acil durum bildirimi gönderme fonksiyonu
function sendEmergencyAlert() {
  const button = document.querySelector(".emergency-button");
  const userId = button.getAttribute("data-user-id");
  const csrfToken = document.querySelector("[name=csrf-token]").content;

  if (navigator.geolocation) {
    // Kullanıcı konumunu al
    navigator.geolocation.getCurrentPosition(
      function (position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        // Bildirimi gönder
        fetch("/send-emergency-email/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({
            user_id: parseInt(userId),
            latitude: latitude,
            longitude: longitude,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert("Acil durum bildiriminiz gönderildi.");
              loadEmergencyAlerts(); // Bildirimler güncelleniyor
            } else {
              alert("Acil durum bildirimi gönderilirken bir hata oluştu.");
            }
          })
          .catch((error) => {
            console.error("Hata:", error);
            alert("Acil durum bildirimi gönderilirken bir hata oluştu.");
          });
      },
      function (error) {
        alert("Konum alınamadı. Lütfen konum izni verdiğinizden emin olun.");
      }
    );
  } else {
    alert("Tarayıcınız konum servisini desteklemiyor.");
  }
}
