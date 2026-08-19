# Hood Law — qayta dizayn

`rshoodlaw.com` sayti uchun 0'dan yozilgan, zamonaviy va yorqin qayta dizayn.
Asl saytdagi barcha matn va ma'lumotlar (xizmatlar, ofis manzillari, telefon
raqamlari) o'zgartirilmagan holda saqlangan — faqat vizual dizayn yangilangan.

## Sahifalar

- `index.html` — bosh sahifa
- `contact.html` — "Contact Me" sahifasi (forma + ofis manzillari)

Ikkalasi ham o'zida barcha narsani (CSS + JS) mujassam etgan mustaqil
fayllar. Tashqi kutubxona yoki build jarayoni kerak emas.

## Ishlatish

Fayllarni to'g'ridan-to'g'ri brauzerda oching yoki istalgan statik
hosting'ga (Netlify, Vercel, GitHub Pages, cPanel va h.k.) yuklang.

## ⚠️ Deploy qilishdan oldin: kontakt formasi

`contact.html`dagi forma hozircha hech qanday backend'ga ulanmagan. Yuborish
tugmasi bosilganda tashrif buyuruvchining email ilovasi (mailto:) ochiladi,
xabar oldindan to'ldirilgan holda. Bu ishlaydi, lekin ikkita narsani hal
qilish kerak:

1. `contact.html` faylida `CONTACT_EMAIL` o'zgaruvchisini (`your-email@rshoodlaw.com`)
   firmaning haqiqiy elektron pochtasiga almashtiring
2. Agar mailto: o'rniga forma to'g'ridan-to'g'ri serverga yuborilishini
   xohlasangiz, [Formspree](https://formspree.io) yoki
   [Netlify Forms](https://www.netlify.com/platform/core/forms/) kabi
   xizmatlardan foydalanib, `contactForm`ning submit handler'ini
   almashtiring

## Xususiyatlari

- To'liq responsive (mobil, planshet, desktop)
- Yorug' va qorong'i rejimni qo'llab-quvvatlaydi
- Xizmat turlari uchun maxsus chizilgan SVG ikonalar
- Google Fonts: Fraunces (sarlavhalar) + Public Sans (matn)

## Keyingi qadamlar

- `Terms of Use`, `Privacy Policy`, `Anti-spam` havolalari hozircha bo'sh
  (`#`) — haqiqiy sahifalar mazmuni berilsa, ular ham qo'shiladi
- Agar saytda qo'shimcha sahifalar (masalan, advokat haqida to'liq bio)
  bo'lsa, ularning kontenti asosida qo'shimcha bo'limlar yaratish mumkin
