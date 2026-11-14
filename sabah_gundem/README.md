# Sabah Gündemi — blackartistanbul

blackartistanbul hesabının her sabah paylaşılan haber/gündem serisi. Tasarım: "Gazete" şablonu (krem zemin, Playfair Display + Inter, kırmızı etiket, altta üç rakam). İlk gönderi: 14 Kasım 2026 (Booker).

## Akış
1. **Pazar akşamı** (zamanlanmış görev): gelecek haftanın 7 gönderisi (pzt–paz) hazırlanır, `hafta-YYYY-MM-DD/` klasörüne (tarih = haftanın pazartesisi) görseller ve `plan.json` yüklenir, paket kullanıcıya gösterilir. Kullanıcı onay verince ilgili kayıtların `onay` alanı `true` yapılıp push edilir.
2. **Her sabah 08:52** (zamanlanmış görev): o güne ait, `onay: true` ve `paylasildi: false` olan kayıt Windsor ile akışta paylaşılır (`create_image_post`), hemen ardından aynı içeriğin hikâye sürümü (`gorsel` adının sonuna `_hikaye` eklenmiş dosya) `create_story` ile paylaşılır. `paylasildi: true`, `media_id` ve `hikaye_paylasildi: true` yazılıp push edilir. Onaysız kayıt asla paylaşılmaz.

## plan.json biçimi
```json
{
  "hafta": "2026-11-16",
  "gonderiler": [
    {
      "tarih": "2026-11-16",
      "gorsel": "hafta-2026-11-16/01_pzt.jpg",
      "caption": "...",
      "kaynaklar": ["https://..."],
      "onay": false,
      "paylasildi": false,
      "media_id": null,
      "hikaye_paylasildi": false
    }
  ]
}
```
Görsel URL'si: `https://raw.githubusercontent.com/aygungulcan96-netizen/blackartistanbul-gorseller/main/sabah_gundem/<gorsel>`

## Görsel üretimi
`python3 sablon/uret.py girdi.json cikti.jpg` — girdi alanları `sablon/uret.py` başındaki açıklamada. Her çalıştırma iki dosya üretir: `cikti.jpg` (akış, 1080x1350) ve `cikti_hikaye.jpg` (hikâye, 1080x1920). Başlık uzunsa yazı otomatik küçülür; "UYARI" çıkarsa metni kısalt.

## İçerik kuralları
- Hesap bağımsız bir edebiyat hesabıdır: hesap sahibinden, onun kitaplarından ya da yayınevinden söz edilmez.
- Odak Türk yayıncılık/edebiyat; dünya edebiyatından büyük haberler de olabilir.
- Her olgu en az bir güvenilir kaynakla doğrulanır; tarihi belirsiz haber kullanılmaz. Kartın altına "Kaynak: …" yazılır.
- Kategori etiketleri: ÖDÜL, YENİ KİTAP, ÇEVİRİ, YIL DÖNÜMÜ, ANMA, FUAR, FESTİVAL, SEKTÖR, SÖYLEŞİ.
- Açıklama: kancayla başlar, 2 kısa paragraf, takipçiye soru, sonra 10-14 hashtag. Amaç olabildiğince geniş kitleye erişmek: konuya özel etiketler (kişi, eser, ödül, etkinlik adları ve bunların yaygın yazılışları) + geniş kitle etiketleri (#Kitap #Bookstagram #KitapKurdu #KitapÖnerisi #Edebiyat #TürkEdebiyatı) + sabit #EdebiyatGündemi. Uzun alıntı yok.
