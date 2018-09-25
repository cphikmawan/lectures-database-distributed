# Partisi Basis Data

#### 05111540000119 - Cahya Putra Hikmawan

### Outline
[1. Deskripsi Server](#1-deskripsi-server)

[2. Implementasi Partisi 1: Sakila DB](#2-implementasi-partisi-1-sakila-db)

- [2.1 - Deskripsi Dataset](#21-deskripsi-dataset)
- [2.2 - Proses Pembuatan Partisi](#22-proses-pembuatan-partisi)
- [2.3 - Benchmarking](#23-benchmarking)

[3. Implementasi Partisi 2: Measures Dataset](#3-implementasi-partisi-2:-measures-dataset)

- [3.1 - Deskripsi Dataset](#31-deskripsi-dataset)
- [3.2 - Import Dataset](#32-import-dataset)
- [3.3 - Benchmarking](#33-benchmarking)

[Kesimpulan](#kesimpulan)

### 1. Deskripsi Server
|||
| --- | --- |
| Sistem Operasi | Ubuntu Server 18.04.1 LTS |
| Versi MySQL | 5.7.23 |
| RAM | 512 MB |
| CPU | 1 Core |

### 2. Implementasi Partisi 1: Sakila DB
#### 2.1 Deskripsi Dataset
Import [sakila-db](assets/sakila-db "Sakila DB") :
```sh
mysql -ucloudy -p < sakila-schema.sql
```
```sh
mysql -ucloudy -p < sakila-data.sql
```
- Dataset ini terdiri dari 23 tabel
```SQL
SELECT TABLE_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'sakila' ORDER BY TABLE_ROWS DESC;
```
- Masing-masing tabel memiliki jumlah baris data sebagai berikut :

| TABLE_NAME | TABLE_ROWS |
| --- | --- |
| payment | 16049 |
| rental | 16044 |
| film_actor | 5462 |
| inventory | 4581 |
| film | 1000 |
| film_text | 1000 |
| film_category | 1000 |
| address | 603 |
| city | 600 |
| customer | 599 |
| actor | 200 |
| country | 109 |
| category | 16 |
| language | 6 |
| store | 2 |
| staff | 2 |
| nicer_but_slower_film_list | NULL |
| customer_list | NULL |
| staff_list | NULL |
| sales_by_store | NULL |
| actor_info | NULL |
| sales_by_film_category | NULL |
| film_list | NULL |

#### 2.2 Proses Pembuatan Partisi 
- Pemilihan tabel yang akan dipartisi
    - Bagaimana cara pemilihan tabel yang akan dibuat partisi?
    Pemilihan tabel yang akan dipartisi ditentukan oleh jumlah data yang paling banyak dan memiliki peluang akan bertambah secara berkala.
- Daftar tabel yang akan dipartisi
    - Tabel Payment
    - Tabel Rental

##### Tabel Payment
- Jenis partisi yang digunakan: **HASH**
- Sehingga tidak memerlukan syarat/predikat.
- Tabel akan dipartisi menjadi **5** bagian yaitu :
    - p1 = 
    - p2 = 
    - p3 = 
    - p4 = 
    - p5 = 

##### Tabel Rental
- Jenis partisi yang digunakan: **HASH**
- Sehingga, tidak memerlukan syarat/predikat.
- Tabel akan dipartisi menjadi **5** bagian yaitu :
    - p1 = 
    - p2 = 
    - p3 = 
    - p4 = 
    - p5 = 

##### Implementasi Partisi
- Script SQL untuk partisi tabel **payment**
```SQL
Tuliskan SQL script yang berisi pembuatan tabel-tabel partisi
```
- Script SQL untuk partisi tabel **rental**
```SQL
Tuliskan SQL script yang berisi pembuatan tabel-tabel partisi
```

#### 2.3 Benchmarking
##### Insert beberapa data baru(minimal 10)
- partisi 1
```SQL
Syntax insert
```
- partisi 2
```SQL
Syntax insert
```
##### Lakukan select data 1 dari partisi benar(partisi 1)
![Gambar](assets/images/partisi_benar.png "Partisi Benar")
##### Lakukan select data 1 dari partisi salah
![Gambar](assets/images/partisi_salah.png "Partisi Salah")

### 3. Implementasi Partisi 2: Measures Dataset
#### 3.1 Deskripsi Dataset
##### Deskripsi Singkat
##### Sumber Dataset
[Download Dataset]()
#### 3.2 Import Dataset
##### Cara Import Dataset 
#### 3.3 Benchmarking
##### SELECT Bendhmarking
##### BIG DELETE Benchmarking

### Kesimpulan