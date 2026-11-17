# Berlin Konuşuyor – Yayın stratejisi (sabah + akşam)

Bu dosya iki günlük görevin (07:52 sabah, 19:27 akşam; paylaşımdan ~30 dk önce) ve haftalık raporun ortak kural kitabıdır. Değişiklik buraya yazılır, görevler her çalışmada bu dosyayı okur.

## 1. İki baskı, iki farklı görev

| | Sabah · "Berlin Gündemi" (07:52 üretim → 08:30 paylaşım) | Akşam · "Berlin Akşamı" (19:27 üretim → 20:00 paylaşım) |
|---|---|---|
| Soru | Bugün ne oluyor, neye dikkat etmeliyim? | Bugün ne oldu, yarın ne var? |
| Zaman penceresi | Son 24 saat + bugünün planlı olayları | Bugün 08:00'den sonra yayımlanan haberler + yarının planlı olayları |
| Kart 1 | Günün en önemli haberi | **Günün gelişmesi**: bugün içinde kesinleşen/değişen en önemli olay |
| Kart 2 | Berlin yerel (ulaşım, kent, hava) | **Yarın Berlin'de**: BVG/S-Bahn, hava (DWD), son başvuru tarihleri, etkinlikler – somut tarih/saatle |
| Kart 3 | Topluluk / Almanya / dünya | **Topluluk & Günün sorusu**: toplulukla ilgili haber ya da izleyiciye sorulacak tek soru (anket için) |
| Stil | Ayın stili (config.json) | Listede bir sonraki stil (akşam farklı görünür) |

## 2. Tekrar etmeme kuralları

1. **Hikâye anahtarı (`key`)**: Her haberin `key` alanı vardır: küçük harf, tireli, 3–5 kelime, kalıcı konu kimliği (ör. `berlin-koalisyon-rgr`, `bvg-grev-aralik`, `vatandaslik-yasasi-degisiklik`). Aynı konu aynı anahtarı alır.
2. **Kontrol listesi**: Yeni baskıdan önce son 7 günün tüm `data/*.json` dosyaları (sabah + akşam) okunur, kullanılmış `key` listesi çıkarılır.
3. **Aynı anahtar = yasak**, şu istisna hariç: **somut yeni bir gelişme** varsa (karar çıktı, tarih değişti, rakam açıklandı, resmî duyuru yapıldı). O zaman:
   - `update_of` alanına eski anahtar yazılır,
   - başlık yeni gelişmeyi söyler (ör. "Koalisyon: ilk karar çıktı"), etiket `GÜNCELLEME` olur,
   - metnin ilk cümlesi neyin değiştiğini söyler. "Hâlâ sürüyor" tipi güncellemeler yasak.
4. **Aynı gün içinde**: Akşam, sabahın 3 haberini tekrar etmez; yalnızca kural 3'teki gibi gün içinde gerçekten değiştiyse "Günün gelişmesi" kartında güncelleme olarak girer.
5. **Çeşitlilik kotası (7 gün)**: Aynı etiket (ör. SİYASET) 7 günde en fazla 5 kez; her baskıda en az 1 kart doğrudan Berlin'deki gündelik hayatla ilgili olmalı; haftada en az 3 kart Türk toplumuna özgü olmalı.
6. **Kaynak tekrarı**: Bir baskıdaki 3 haberin üçü de aynı yayın kuruluşundan gelemez.

## 3. Güncellik kuralları

1. **Yayım saati kontrolü**: Her haberin kaynak yayım zamanı kontrol edilir. Sabah: son 24 saat. Akşam: bugün 08:00'den sonra (ya da yarın için planlı olay).
2. **Planlı olaylar**: "Yarın Berlin'de" kartı yalnızca tarihi ve saati kesin olan, resmî ya da güvenilir kaynakta duyurulmuş olayları içerir.
3. **Bayat haber yasak**: 48 saatten eski bir olay, yalnızca yeni gelişme varsa (kural 2.3) girer.
4. **Doğrulama**: Her haber ≥2 bağımsız kaynak ya da 1 resmî kaynak (`sources_n`). Tek kaynaklı ya da hassas (`sensitive`) haber → onay zorunlu.
5. **Sessiz gün**: Kriterlere uyan 3 haber yoksa uydurma/zorlama yok: 2 kart + "Yarın Berlin'de" kartıyla yetinilir.

## 4. Dil ve ton

- Kendi cümlelerimiz; kaynaktan cümle kopyalanmaz, rakam ve alıntı uydurulmaz.
- Başlık ≤ 45 karakter, metin ≤ 230 karakter, "Sana etkisi" ≤ 110 karakter ve somut olmalı (ne yapmalı / kimi etkiler / ne zaman).
- Süre otomatik: her story en az 15 sn, okuma süresine göre (≈2,4 kelime/sn) en fazla 45 sn. Sağ üstte geri sayım halkası, altta telifsiz prosedürel fon müziği (sabah majör, akşam minör) motor tarafından eklenir.
- Tarafsız; siyasi değerlendirme yok. Suç, ölüm, din, kutuplaştırıcı siyaset → `sensitive: true`.

## 5. JSON alanları

```
{"iso":"YYYY-MM-DD","edition":"sabah|aksam","needs_approval":true,
 "items":[{"key":"...","update_of":null,"tag":"...","title":"...","body":"...","etki":"...",
           "source":"...","sources_n":2,"sensitive":false,"published":"YYYY-MM-DDTHH:MM"}]}
```
