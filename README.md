🔦 Akıllı Oda Aydınlatma Sistemi – Raspberry Pi Tabanlı
📌 Proje Amacı
Bu proje, bir odaya girildiğinde ortam ışığına bağlı olarak otomatik olarak bir lambayı (LED) yakmayı ve içeride biri kalmadığında kapatmayı amaçlamaktadır. Sistem, fotosel (LDR), ultrasonik mesafe sensörü (HC-SR04) ve USB kamera ile insan varlığını tespit eder.

🛠️ Kullanılan Donanım
Raspberry Pi (GPIO destekli)

HC-SR04 Ultrasonik Mesafe Sensörü

LDR (Fotosel) + 10kΩ direnç

LED (veya röle modülü ile lamba)

USB Kamera (UVC uyumlu)

Jumper kablolar, breadboard

⚙️ Sistem Nasıl Çalışır?
1. Işık Seviyesi Kontrolü (Fotosel ile)
Odanın ışık seviyesi ölçülür.

Eğer ortam aydınlıksa sistem pasif olur (LED yakılmaz).

Ortam karanlıksa sistem devreye girer ve diğer kontroller başlar.

2. Giriş Tespiti (HC-SR04 ile)
Sensör, oda kapısının girişine yerleştirilmiştir.

60 cm’den daha yakın bir hareket algılanırsa biri girdiği varsayılır.

Bu durumda LED yakılır ve son görülen zaman kaydedilir.

3. İnsan Tespiti (OpenCV ile Kamera Analizi)
Kamera görüntüsü işlenir, OpenCV HOG + SVM ile insan varlığı algılanır.

İnsan tespit edilirse LED açık kalmaya devam eder.

15 saniye boyunca insan algılanmazsa LED otomatik olarak kapatılır.

4. Kullanıcı Müdahalesi
Program çalışırken "q" tuşuna basarak çıkış yapılabilir.

Ctrl+C ile de terminalden çıkılabilir.

🖥️ Görsel Arayüz
Program çalışırken kamera görüntüsü açılır. Tespit edilen insanlar kare içine alınarak kullanıcıya gösterilir.

📂 Kod Yapısı
Ana Python dosyasında:

GPIO pin tanımları

LDR okuma fonksiyonu

Mesafe ölçüm fonksiyonu

OpenCV ile insan tespiti

Zaman tabanlı LED kontrol sistemi

🚪 Sensör Konumlandırması
LDR: Odanın genel ışık seviyesini algılayacak şekilde yerleştirilir.

HC-SR04: Kapının giriş kısmına bakacak şekilde monte edilir, böylece içeri giren kişi algılanır.

Kamera: Oda içine bakacak şekilde yerleştirilir, insanları görsel olarak tespit eder.

🧠 Genişletme Fikirleri
Hareket sensörü (PIR) ile desteklenebilir.

Akıllı ev sistemine MQTT veya HTTP API üzerinden bağlanabilir.

Kamera ile yüz tanıma eklenebilir.

LED yerine bir röle bağlanarak gerçek bir lamba kontrol edilebilir.

📸 Ekran Görüntüsü
Kamera ile alınan görüntülerde tespit edilen insanlar yeşil dikdörtgen ile işaretlenir.
