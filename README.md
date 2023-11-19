# Tugas Besar Aljabar Linier dan Geometri : Sistem Persamaan Linier, Determinan, dan Aplikasinya

## Deskripsi Umum
Repository Tugas Besar 2 Aljabar Linier dan Geometri: CONTENT-BASED INFORMATION RETRIEVAL (CBIR). <br>
Web dibangun menggunakan Flask Python dan Bootstrap5 HTML CSS.

### Anggota Kelompok:
| Nama  | NIM |
| ------------- | ------------- |
| Maulana Muhamad Susetyo |  13522127 |
| Ahmad Rafi Maliki |  13522137 |
| Andi Marihot Sitorus |  13522139 |

## Cara Penggunaan:

### Commands
```
# Clone repository github
git clone https://github.com/rafimaliki/Algeo02-22127.git

# CD ke folder src
cd src

# Start server lokal
py main.py

# Buka http://127.0.0.1:5000 pada browser
```

### Prerequisite
```
# Modul python yang harus diinstal
pip install Flask
pip install numpy
pip install requests
pip install beautifulsoup4
```

## Fitur
* **CBIR Metode Color** <br>
Proses pencarian gambar yang memiliki similaritas > 60% menggunakan metode cbir color
* **CBIR Meotode Tekstur** <br>
Proses pencarian gambar yang memiliki similaritas > 60% menggunakan metode cbir tekstur
* **Input Dataset dari Local File** <br>
Metode perolehan dataset dengan upload dari local file
* **Scraping Dataset dari Web** <br>
Metode perolehan dataset dengan web scraping


## Struktur Folder:
```
├─ doc\
├─ img\
├─ src\
│  ├─ website\
│  │  ├─ static\
│  │  │  ├─ assets\
│  │  │  ├─ dataset_picture\
│  │  │  └─ submitted_picture\
│  │  ├─ templates\
│  │  │  ├─ base.html
│  │  │  ├─ page_aboutus.html
│  │  │  ├─ page_camerainput.html
│  │  │  ├─ page_home.html
│  │  │  └─ page_userinput.html
│  │  ├─ __init__.py
│  │  ├─ function_cbir_color.py
│  │  ├─ function_cbir_texture.py
│  │  ├─ function_webscrap.py
│  │  ├─ page_aboutus.py
│  │  ├─ page_camerainput.py
│  │  ├─ page_home.py
│  │  └─ page_userinput.py
│  └─ main.py     
├─ test\
└─ README.md
```
