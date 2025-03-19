# README: XSOAR Automation Prerequisites

## Prerequisites
Untuk menjalankan automation script ini di XSOAR, diperlukan custom Docker image karena library `openpyxl` dan `Pillow` tidak tersedia secara default di XSOAR.

### 1. Persiapan Custom Docker Image

1. **Buat file `requirements.txt`** dengan isi berikut:
   ```
   openpyxl
   pillow
   ```
2. **Buat Dockerfile** dengan konten berikut:
   ```Dockerfile
   FROM demisto/python3:3.11.10.116439
   COPY requirements.txt /
   RUN pip install --no-cache-dir -r /requirements.txt
   ```
3. **Build dan push image ke registry**
   ```sh
   docker build -t your-registry.com/your-image-name:latest .
   docker push your-registry.com/your-image-name:latest
   ```

### 2. Konfigurasi di XSOAR

#### **2.1 Menambahkan Registry di XSOAR**
1. **Buka XSOAR GUI**
2. Navigasi ke `Settings & Info > Advanced > Image Registry`
3. Pada **Registry Setting**, pilih:
   - **Direct**, jika menggunakan Docker Hub: `docker.io`
   - **Engine**, jika menggunakan private registry:
     - Masukkan `devsecops-registry.dinamikasolusi.com` atau alamat IP jika tidak ada DNS

#### **2.2 Menggunakan Custom Image di Automation Script**
1. Buka **Automation Script** di XSOAR
2. Pada bagian **Docker image name**, masukkan:
   ```
   your-registry.com/your-image-name:latest
   ```
3. Simpan dan jalankan automation script

### Troubleshooting
- **Timeout saat menjalankan script?**
  - Pastikan koneksi ke registry dapat diakses dari XSOAR.
  - Cek apakah image telah di-push dengan benar.
- **Error `ModuleNotFoundError: No module named 'openpyxl'`?**
  - Pastikan `requirements.txt` sudah berisi `openpyxl` dan `Pillow` sebelum build image.
  - Cek apakah XSOAR sudah menggunakan image yang benar di setting Docker image name.

Jika ada kendala lain, silakan periksa log XSOAR atau hubungi administrator DevSecOps Anda.

