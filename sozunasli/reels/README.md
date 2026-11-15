# Sözün Aslı — günlük Reels

Her gün 12:00'de (Europe/Istanbul) @sozunasli_ hesabında bir Reels yayınlanır. Bu, günün diğer planlı gönderilerine (09:00 karusel, 13:00 hikâye, 19:30 gönderi, 21:00 hikâye) EK olarak paylaşılır.

## Dosyalar
- `rNN_<kelime>.mp4` — yayınlanan/yayınlanacak videolar (NN: sıra no, 01'den başlar)
- `plan.json` — her Reels'in kaydı: no, tarih, kelime, dosya, caption, kaynaklar, onay, paylasildi, media_id
- `sablon/r01_dolap.html` — referans şablon (tasarım, zamanlama, animasyonlar). Yeni Reels için kopyala, yalnızca metni değiştir.
- `sablon/yap.sh` — `bash sablon/yap.sh <html> <çıktı.mp4> <süre>` fontları hazırlar, kareleri çizer, MP4 üretir.

## Kurallar
- Tasarım: krem zemin, lacivert mürekkep, terrakota vurgu, altın ok; Playfair Display + Inter. Üstte "SÖZÜN ASLI" ve "REELS · NN", tepede ilerleme çubuğu.
- Yapı (4 sahne, ~22,5 sn): 1) merak kancası + büyük kelime, 2) köken (kaynak dil → Türkçe) ve ilk anlam, 3) bugün dilde kalan izler / şaşırtıcı bağlantı, 4) "Kökü seni şaşırtan başka hangi kelime var? Yorumlara yaz" + hesap.
- Süre 20–25 sn. Her satır en az ~2,5 sn okunur kalmalı (Can daha hızlısını "çok hızlı" buldu).
- İçerik alt ~450 px'e ve sağ kenara girmemeli (Instagram arayüzü kapatır).
- Kelime: `sozunasli/kelimeler.json`'daki kullanılmış kelimelerden ve aynı haftanın carousel kelimelerinden farklı olmalı.
- 15 Kasım 2026'dan itibaren Reels'ler haftalık paketle hazırlanır ve `sozunasli/hafta-*/plan.json` üzerinden paylaşılır (bkz. `sozunasli/README.md`). Bu klasördeki `plan.json` yalnızca R01 kaydı için tutuluyor; yeni kayıtlar haftalık plana yazılır.
- Köken en az iki güvenilir kaynakla (TDK, Nişanyan, akademik makale) doğrulanır; tartışmalıysa ihtiyatlı ifade edilir. Doğrulanamayan kelime kullanılmaz.
- Hesap sahibinden veya kitaplarından söz edilmez. Fotoğraf kullanılmaz; yalnızca tipografi ve basit çizimler.
- Paylaşım yalnızca Can'ın onayladığı (onay:true) kayıtla yapılır.
