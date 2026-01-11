# 🌿 Klasifikasi Daun Herbal

Aplikasi web klasifikasi daun herbal menggunakan CNN (MobileNetV2) dan Google Gemini AI untuk informasi khasiat.

## 📋 Deskripsi

Project Computer Vision berbasis Flask untuk identifikasi 8 jenis tanaman obat. Menggunakan Deep Learning (MobileNetV2) untuk klasifikasi citra dan Gemini API untuk generate wawasan kesehatan herbal secara otomatis.

Aplikasi ini dapat mengidentifikasi 8 jenis daun herbal:
- **Bangun-bangun**
- **Jambu Biji**
- **Lidah Buaya**
- **Mint**
- **Pandan**
- **Pegagan**
- **Sirih**
- **Sirsak**

## 🚀 Cara Menjalankan

### 1. Persiapan Environment

Pastikan Python 3.8+ sudah terinstall, kemudian install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Struktur Project

Pastikan struktur folder seperti ini:

```
project/
├── app.py
├── mobilenetv2_daun_v2.h5
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── uploads/
```

### 3. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

## 💻 Cara Menggunakan

1. Buka browser dan akses `http://localhost:5000`
2. Klik area upload atau drag & drop gambar daun
3. Preview gambar akan muncul
4. Klik tombol **"Prediksi Jenis Daun"**
5. Hasil prediksi akan ditampilkan dengan:
   - Nama jenis daun
   - Tingkat keyakinan (confidence score) dalam persen
   - Informasi khasiat dari AI

## 🎨 Fitur UI

- **Desain Modern & Minimalis**: Interface yang bersih dan mudah digunakan
- **Tema Hijau Herbal**: Warna hijau yang menenangkan dan sesuai tema
- **Drag & Drop Upload**: Upload gambar dengan mudah
- **Image Preview**: Lihat gambar sebelum prediksi
- **Integrasi AI**: Penjelasan khasiat tanaman powered by Google Gemini

## 🔧 Teknologi

- **Backend**: Flask (Python)
- **Deep Learning**: TensorFlow/Keras
- **Model**: MobileNetV2 (Transfer Learning)
- **AI Integration**: Google Gemini API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 📄 Lisensi

Project ini dibuat untuk keperluan edukasi.

---

**Powered by MobileNetV2 • TensorFlow & Flask • Google Gemini**
