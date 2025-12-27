# bilgisayar-aglarinda-temel-protokoller-proje

## HTTP2 ve QUIC Performans Karşılaştırması

Bu proje, **HTTP2** ve **QUIC** protokollerinin farklı ağ koşulları 
(gecikme ve paket kaybı) altında performans karşılaştırmasını yapmak
amacıyla geliştirilmiştir. 

Çalışmada, yapay ağ koşulları oluşturmak için **NETEM** aracı
kullanılmıştır.

### Proje Dosyaları

- `cert.pem`
- `hypercorn_config.py`
- `key.pem`
- `requirements.txt`
- `server.key`
- `tcp_yeni_client.py`
- `tcp_yeni_server.py`         

### Gereksinimler

- Python 3.x
- Gerekli Python kütüphaneleri (requirements.txt'te belirtilen)
- Linux ortamı (Netem için)  

### Çalıştırma Adımları

1- HTTP2 Testi

Sunucuyu başlat:
```bash
hypercorn -c hypercorn_config.py tcp_yeni_server:app --log-level debug
```

İstemciyi çalıştır:
```bash
python tcp_yeni_client.py
```

2-Netem ile Ağ Koşulları Oluşturma: 

- NetEm Başlama:
```bash
sudo tc qdisc add dev lo root netem delay 100ms loss 1%
```
- NetEm Kaldırma:
```bash
sudo tc qdisc del dev lo root
```  
