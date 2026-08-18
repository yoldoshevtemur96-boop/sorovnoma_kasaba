# sorovnoma_kasaba

Kasaba uyushmasi a'zolari uchun oddiy so'rovnoma (survey) vositasi.
Faqat Python standart kutubxonasidan foydalanadi — qo'shimcha
paketlarni o'rnatish shart emas (Python 3.8+ talab qilinadi).

## Imkoniyatlari

- Yopiq (variantli) va ochiq (erkin matnli) savollar bilan so'rovnoma yaratish
- Ishtirokchilar javoblarini validatsiya qilib qabul qilish
- Har bir savol bo'yicha natijalarni sanash (`tally`/`summary`)
- So'rovnomani JSON faylga saqlash va undan qayta yuklash

## Ishga tushirish

```bash
python3 main.py
```

Bu namunaviy so'rovnoma yaratib, ikkita javobni qo'shadi va natijalar
xulosasini ekranga chiqaradi.

## Testlarni ishga tushirish

```bash
python3 -m unittest discover -s sorovnoma/tests -t .
```

## Kod orqali foydalanish

```python
from sorovnoma.survey import Question, Survey

survey = Survey(title="A'zolar so'rovnomasi")
survey.add_question(
    Question(id="mamnuniyat", text="Mamnunmisiz?", options=["Ha", "Yo'q"])
)
survey.submit_response({"mamnuniyat": "Ha"})

print(survey.tally("mamnuniyat"))
# Counter({'Ha': 1})

survey.save("natijalar.json")
```
