DATA_TO_SEND = b"X" * 10240  # 10KB veri -> Göndereceğimiz ham binary veri, 10.240 adet "X" byte'ı

async def app(scope, receive, send):
    """Basit bir ASGI uygulaması."""
    assert scope['type'] == 'http'  # Bu uygulamanın sadece HTTP isteklerini kabul ettiğini garanti eder
    
    status_code = 200  # HTTP yanıt durumu (OK)
    content_length = len(DATA_TO_SEND)  # Gönderilecek veri boyutu hesaplanıyor

    # -------------------------------
    # 1) HTTP Yanıt Başlığını Gönder
    # -------------------------------
    # ASGI protokolünde bir yanıt iki aşamada gönderilir:
    #  - http.response.start → Başlıklar
    #  - http.response.body  → Gövde (body)
    await send({
        'type': 'http.response.start',  # Başlık gönderme olayı
        'status': status_code,          # HTTP durum kodu
        'headers': [
            [b'content-type', b'application/octet-stream'],  # Binary veri tipi
            [b'content-length', str(content_length).encode()],  # Gövde uzunluğu (byte)
        ],
    })

    # -------------------------------
    # 2) HTTP Gövdesini Gönder
    # -------------------------------
    # Tek seferde 10KB veriyi gönderiyoruz
    await send({
        'type': 'http.response.body',  # Gövde gönderme olayı
        'body': DATA_TO_SEND,          # Gönderilecek veri
        'more_body': False,            # Body'nin devamı olmadığı bilgisini verir
    })

    # -------------------------------
    # 3) Loglama → Konsola bilgi yaz
    # -------------------------------
    # HTTP/2 sunucusunda gelen isteğin path’i, durum kodu ve gönderilen veri boyutunu yazdırıyoruz
    print(f"[HTTP/2 SUNUCU] İstek tamamlandı → "
          f"Path: {scope['path']}, Status: {status_code}, Boyut: {content_length} byte")

