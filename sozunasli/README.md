# Sözün Aslı (@sozunasli_) — haftalık paket düzeni

Türkçe etimoloji Instagram hesabı. Hesap: Windsor.ai connector `instagram`, account **17841474055038364**.
(Aynı depodaki blackartistanbul hesabı 17841459815006761 ile KARIŞTIRMA.)
Hesap sahibinden, onun kitaplarından ya da yayınevinden ASLA söz edilmez.

## İşleyiş
1. **Pazar akşamı** "haftalık paket" görevi gelecek haftayı (pazartesi–pazar) hazırlar, `hafta-<pazartesi tarihi>/plan.json` yazar (her kayıt `onay:false`), Can'a tek seferde sunar. Can onaylayınca kayıtlar `onay:true` olur.
2. **Her gün** "günlük paylaşım" görevi o anki saate gelmiş, `onay:true` ve `paylasildi:false` kayıtları paylaşır, `paylasildi:true` + `media_id` yazar.
3. Onaylanmamış hiçbir şey paylaşılmaz.

## Günlük düzen (Europe/Istanbul)
| saat | tur | içerik |
|---|---|---|
| 09:00 | carousel | Günün 1. kelimesi, 5 kare. Son kare: önceki günün 13:00 sorusunun cevabı + okura soru. |
| 12:00 | reels | Günün 2. kelimesi (~22,5 sn). Kurallar: `reels/README.md`, şablon: `reels/sablon/`. |
| 13:00 | story | "Yarının kelimesi" sorusu (ertesi günün 09:00 carousel kelimesi, 3 seçenek, "Cevap yarın sabah"). |
| 19:30 | image | Günün teması (aşağıda). |
| 20:30 | comment | Yalnızca 19:30 gönderisi bir quiz ise: cevap, o gönderiye ilk yorum. |
| 21:00 | story | "Bugün öğrendik": günün carousel'inden mini sınav, doğru şık işaretli (`"dogru"`). |

Haftanın son günü (pazar) 13:00 hikâyesi, gelecek pazartesinin carousel kelimesini duyurur → haftalık paket gelecek pazartesinin kelimesini de seçip `kelimeler.json` → `planlandi` içine yazar (soru ve doğru cevap notuyla).

### 19:30 temaları
Pzt: Hangisi Türkçe? (quiz + 20:30 cevap yorumu) · Sal: Göçmen kelimeler (Türkçeden dünyaya) · Çar: Yanlış bilinenler · Per: Deyimin aslı · Cum: Aynı kökten (kelime aileleri) · Cmt: Haftanın büyük quiz'i (+ 20:30 cevap yorumu) · Paz: Haftanın özeti (haftanın 14 kelimesinden seçmeler, tek kare).

## Görsel üretimi
`python3 sozunasli/sablon/gen.py <girdi.json> <çıktı_klasörü>` → her öğe için `<ad>.jpg`.
Tipler ve alanlar için `sablon/ornek/ornek_gun.json` (kapak, metin, soru, story) ve `ornek_aksam.json`'a bak.
- Gönderiler 1080x1350, hikâyeler 1080x1920, JPEG.
- `<em>` vurgu (terrakota), `<b>` kalın, `<br>` satır. Metinler kısa; her görseli Read ile aç, taşma/hatalı Türkçe karakter kontrol et.
- Kimlik: krem kâğıt zemin, lacivert mürekkep, terrakota vurgu, altın ok; Playfair Display + Inter. Fotoğraf yok.
- Carousel kapağında `no` alanı sıra numarasıdır (001, 002, …; `kelimeler.json`'daki son carousel no + 1).

## plan.json biçimi (`hafta-YYYY-MM-DD/plan.json`, liste)
```json
{
  "id": "2026-11-16_0900",
  "tarih": "2026-11-16", "saat": "09:00",
  "tur": "carousel | reels | story | image | comment",
  "kelime": "lokanta",
  "dosyalar": ["sozunasli/hafta-2026-11-16/pzt_sabah_1.jpg", "..."],
  "caption": "…",                       // carousel, reels, image (story'de yok)
  "hedef_id": "2026-11-16_1930",          // yalnızca comment: yorumun yapılacağı kaydın id'si
  "mesaj": "…",                           // yalnızca comment
  "thumb_offset": 1500,                   // yalnızca reels (ms), kapakta kelimenin tam göründüğü an
  "kaynaklar": ["https://…"],
  "onay": false, "paylasildi": false, "media_id": null
}
```
Dosya adları: `<gün>_<slot>` (pzt, sal, car, per, cum, cmt, paz; slot: sabah_1..5, ogle_hikaye, aksam, aksam_hikaye). Reels: `reels/rNN_<kelime>.mp4` (dosyalar alanına bu yol yazılır).

## Paylaşım (günlük görev için)
- Görsel adresi: `https://raw.githubusercontent.com/aygungulcan96-netizen/blackartistanbul-gorseller/main/<yol>` (önce HTTP 200 kontrol et).
- Reels adresi: `https://cdn.jsdelivr.net/gh/aygungulcan96-netizen/blackartistanbul-gorseller@<son commit>/<yol>`; içerik türü hatasında bir kez raw adresi dene. `share_to_feed: true`.
- Windsor eylemleri: carousel → `create_carousel_post`, reels → `create_video_post`, story → `create_story`, image → `create_image_post`, comment → `create_comment` (media_id = hedef kaydın media_id'si).
- Caption'ı hiç değiştirmeden kullan.
- Sonucu belirsiz hatada TEKRAR DENEMEDEN önce Windsor `get_data` (connector instagram, account 17841474055038364, alanlar media_id, media_caption, media_type, timestamp; hikâyeler için story_id, story_timestamp; date_preset last_1dT) ile paylaşımın olup olmadığını kontrol et.
- Her başarılı paylaşımdan sonra plan.json güncelle, commit + push. Push reddedilirse `git pull --rebase` sonra tekrar push (depoyu blackartistanbul görevleri de kullanıyor).

## Kelime seçimi ve doğruluk
- `kelimeler.json`'daki `kullanildi` kelimeleri ana konu olarak tekrar işlenmez; `deginildi` kelimeleri işlenebilir ama aynı bilgiyle değil.
- Günlük hayatta sık kullanılan, kökeni şaşırtıcı kelimeler. Kaynak dilleri çeşitlendir (Arapça, Farsça, Fransızca, İtalyanca, Rumca, Ermenice, Moğolca, eski Türkçe, Türkçeden dünyaya…).
- Her köken bilgisini en az iki güvenilir kaynakla doğrula (TDK, Nişanyan Sözlük, akademik makaleler). Tartışmalıysa ihtiyatlı yaz ("…olduğu düşünülüyor"); doğrulanamıyorsa o kelimeyi kullanma.
- Kaynak metinlerden uzun alıntı yapma; kendi cümlelerinle yaz.
- Okur yorumlarında önerilen kelimelere öncelik ver.
