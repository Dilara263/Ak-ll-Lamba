# 🔦 Akıllı Oda Aydınlatma Sistemi – Raspberry Pi Tabanlı

## 📌 Proje Amacı

Bu proje, **bir odaya girildiğinde ortam ışığına bağlı olarak otomatik bir lambayı (LED) yakmayı** ve içeride insan kalmadığında kapatmayı amaçlar. Sistem; **fotosel (LDR)**, **ultrasonik mesafe sensörü (HC-SR04)** ve **kamera ile insan tespiti** gibi unsurları kullanır.

## 🛠️ Kullanılan Donanım

- 🧠 Raspberry Pi (GPIO destekli)
- 📏 HC-SR04 Ultrasonik Mesafe Sensörü
- 🌞 LDR (Fotosel) + 10kΩ direnç
- 💡 LED veya Röle (Gerçek lamba kontrolü için)
- 🎥 USB Kamera (UVC uyumlu)
- 🔌 Breadboard, jumper kablolar

## ⚙️ Sistem Çalışma Prensibi

### 1. 🌗 Ortam Işığı Kontrolü (LDR)
- LDR ile ışık seviyesi ölçülür.
- **Eğer ortam aydınlıksa sistem pasif kalır.**
- **Ortam karanlıksa sistem aktif hale gelir.**

### 2. 🚪 Giriş Tespiti (HC-SR04)
- Sensör, **oda kapısı girişine** konumlandırılır.
- 60 cm altındaki hareketler, **birinin içeri girdiği** şeklinde değerlendirilir.
- LED yakılır ve zaman kaydedilir.

### 3. 🧍 İnsan Tespiti (Kamera + OpenCV)
- OpenCV HOG + SVM kullanılarak insan tespiti yapılır.
- İnsan algılanırsa LED açık kalır.
- **15 saniye boyunca kimse algılanmazsa LED kapanır.**

### 4. 🖐️ Manuel Çıkış
- `'q'` tuşuna basarak kamera penceresinden çıkılabilir.
- `Ctrl+C` ile program terminalden sonlandırılabilir.

## 🧭 Sensör Yerleşimi

- **LDR**: Oda genel ışığını algılayacak şekilde yerleştirilir.
- **HC-SR04**: Kapı girişine bakacak şekilde monte edilir.
- **Kamera**: Odanın içini görecek şekilde konumlandırılır.

## 🖥️ Görsel Arayüz

- Kamera görüntüsü ekrana yansıtılır.
- İnsanlar kare içine alınarak kullanıcıya gösterilir.

## 🧠 Genişletme Fikirleri

- 🔄 PIR sensörü entegrasyonu
- 🌐 MQTT veya HTTP ile uzaktan kontrol
- 🧠 Yüz tanıma ile kişisel otomasyon
- 💡 Röle ile gerçek lamba veya cihaz kontrolü

