import httpx
import time
import asyncio
import ssl

HOST = "127.0.0.1"   # Sunucu IP adresi (lokal test)
PORT = 8443          # HTTP/2 + TLS port numarası
COUNT_OF_OBJECTS = 10  # Aynı anda istenecek nesne sayısı (eşzamanlı HTTP/2 stream sayısı)

async def fetch_object(client, object_id):
    # Her nesne için URL oluşturuluyor (sadece id parametresi farklı)
    url = f"/test_file.bin?id={object_id}"
    try:
        # HTTP/2 GET isteği gönderiyoruz (timeout = 30 saniye)
        response = await client.get(url, timeout=30)
        print(f"[HTTP/2 İSTEMCİ] Nesne {object_id} tamamlandı. Boyut: {len(response.content)} byte.")
        return len(response.content)
    except Exception as e:
        # Hata olursa ekrana yaz
        print(f"[HTTP/2 İSTEMCİ] Nesne {object_id} hatası: {e}")
        return 0

async def run_h2_client():
    # ----------------------------
    # TLS Bağlantı Yapılandırması
    # ----------------------------
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False          # self-signed sertifikada host doğrulamayı kapatıyoruz
    ssl_ctx.verify_mode = ssl.CERT_NONE     # sertifika doğrulamasını devre dışı bırak

    start_connect = time.monotonic()  # Başlangıç zamanı (TCP+TLS handshake süresi ölçmek için)

    # ---------------------------------------
    # HTTP/2 İstemcisi (AsyncClient oluşturma)
    # ---------------------------------------
    async with httpx.AsyncClient(
        http2=True,                                     # HTTP/2 aktif
        base_url=f"https://{HOST}:{PORT}",              # Taban URL
        verify=ssl_ctx,                                 # TLS doğrulama ayarı
    ) as client:

        # TCP + TLS handshake toplam süresi
        print(f"--- Bağlantı Süresi (TCP+TLS): {time.monotonic() - start_connect:.4f} saniye ---")

        # ---------------------------------------
        # EŞZAMANLI (CONCURRENT) HTTP/2 İSTEKLERİ
        # ---------------------------------------
        # HTTP/2 multiplexing burada test ediliyor:
        # 10 adet GET isteğini aynı anda gönderiyoruz → 10 farklı stream
        tasks = [asyncio.create_task(fetch_object(client, i)) for i in range(COUNT_OF_OBJECTS)]

        start_download = time.monotonic()  # İndirme başlangıç zamanı

        # Tüm isteklerin aynı anda bitmesini bekle
        sizes = await asyncio.gather(*tasks)

        # Toplam süre ve indirilen toplam veri
        print(f"--- Toplam İndirme Süresi: {time.monotonic() - start_download:.4f} saniye ({sum(sizes)} byte) ---")


if __name__ == "__main__":
    # Async fonksiyonu çalıştır
    asyncio.run(run_h2_client())

