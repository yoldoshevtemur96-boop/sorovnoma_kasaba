"""Kasaba uyushmasi so'rovnomasini yaratish, javoblarni yig'ish va
natijalarni hisoblash uchun asosiy modul.

Ushbu modul tashqi kutubxonalarsiz (faqat standart kutubxona) ishlaydi,
shuning uchun uni istalgan Python 3.8+ muhitida ishlatish mumkin.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Question:
    """So'rovnomadagi bitta savol.

    ``options`` berilsa, savol yopiq (bir nechta variantli) hisoblanadi va
    javob shu variantlardan biri bo'lishi shart. ``options`` bo'sh bo'lsa,
    savol ochiq (erkin matnli) hisoblanadi.
    """

    id: str
    text: str
    options: List[str] = field(default_factory=list)

    @property
    def is_open(self) -> bool:
        return not self.options

    def validate(self, answer: str) -> bool:
        if self.is_open:
            return bool(answer.strip())
        return answer in self.options

    def to_dict(self) -> dict:
        return {"id": self.id, "text": self.text, "options": self.options}

    @staticmethod
    def from_dict(data: dict) -> "Question":
        return Question(id=data["id"], text=data["text"], options=list(data.get("options", [])))


class DuplicateQuestionError(ValueError):
    """Bir xil id bilan savol ikki marta qo'shilganda ko'tariladi."""


class InvalidAnswerError(ValueError):
    """Javob savolning variantlariga mos kelmaganda ko'tariladi."""


class Survey:
    """Savollar to'plami va ishtirokchilar javoblarini boshqaradi."""

    def __init__(self, title: str):
        self.title = title
        self._questions: Dict[str, Question] = {}
        self._responses: List[Dict[str, str]] = []

    # -- savollarni boshqarish -------------------------------------------------
    def add_question(self, question: Question) -> None:
        if question.id in self._questions:
            raise DuplicateQuestionError(f"'{question.id}' savoli allaqachon mavjud")
        self._questions[question.id] = question

    @property
    def questions(self) -> List[Question]:
        return list(self._questions.values())

    # -- javoblarni qabul qilish ------------------------------------------------
    def submit_response(self, answers: Dict[str, str]) -> None:
        """Bitta ishtirokchining javoblarini qo'shadi.

        Har bir savol uchun javob berilishi va variantlarga mos kelishi shart.
        """
        for qid, question in self._questions.items():
            if qid not in answers:
                raise InvalidAnswerError(f"'{qid}' savoliga javob berilmagan")
            if not question.validate(answers[qid]):
                raise InvalidAnswerError(
                    f"'{qid}' savoli uchun noto'g'ri javob: {answers[qid]!r}"
                )
        self._responses.append(dict(answers))

    @property
    def responses(self) -> List[Dict[str, str]]:
        return list(self._responses)

    def response_count(self) -> int:
        return len(self._responses)

    # -- natijalarni hisoblash ---------------------------------------------
    def tally(self, question_id: str) -> Counter:
        """Berilgan savol bo'yicha har bir javob nechta marta kelganini sanaydi."""
        if question_id not in self._questions:
            raise KeyError(f"'{question_id}' savoli topilmadi")
        return Counter(r[question_id] for r in self._responses if question_id in r)

    def summary(self) -> Dict[str, Counter]:
        return {qid: self.tally(qid) for qid in self._questions}

    # -- saqlash va yuklash ---------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "questions": [q.to_dict() for q in self.questions],
            "responses": self._responses,
        }

    def save(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @staticmethod
    def from_dict(data: dict) -> "Survey":
        survey = Survey(title=data["title"])
        for q in data.get("questions", []):
            survey.add_question(Question.from_dict(q))
        for response in data.get("responses", []):
            survey.submit_response(response)
        return survey

    @staticmethod
    def load(path: str | Path) -> "Survey":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return Survey.from_dict(data)


def build_sample_survey() -> Survey:
    """Kasaba uyushmasi a'zolari uchun namunaviy so'rovnoma yaratadi."""
    survey = Survey(title="Kasaba uyushmasi a'zolari so'rovnomasi")
    survey.add_question(
        Question(
            id="mamnuniyat",
            text="Kasaba uyushmasi faoliyatidan qanchalik mamnunsiz?",
            options=["Juda mamnun", "Mamnun", "O'rtacha", "Norozi"],
        )
    )
    survey.add_question(
        Question(
            id="tadbir",
            text="Qaysi tadbirda ishtirok etishni xohlaysiz?",
            options=["Sport musobaqasi", "Malaka oshirish kursi", "Ijtimoiy yordam dasturi"],
        )
    )
    survey.add_question(
        Question(id="taklif", text="Kasaba uyushmasiga takliflaringiz bormi?")
    )
    return survey


def _print_summary(survey: Survey) -> None:
    print(f"\n=== {survey.title} ===")
    print(f"Jami javoblar: {survey.response_count()}\n")
    for question in survey.questions:
        print(f"- {question.text}")
        if question.is_open:
            answers = [r.get(question.id, "") for r in survey.responses if r.get(question.id)]
            for answer in answers:
                print(f"    * {answer}")
        else:
            counts = survey.tally(question.id)
            for option in question.options:
                print(f"    {option}: {counts.get(option, 0)}")
        print()


def main(argv: Optional[List[str]] = None) -> int:
    """Namunaviy so'rovnomani ishga tushirib, natijalarni ekranga chiqaradi."""
    survey = build_sample_survey()
    survey.submit_response(
        {
            "mamnuniyat": "Mamnun",
            "tadbir": "Malaka oshirish kursi",
            "taklif": "Ko'proq onlayn tadbirlar bo'lsa yaxshi bo'lardi",
        }
    )
    survey.submit_response(
        {
            "mamnuniyat": "Juda mamnun",
            "tadbir": "Sport musobaqasi",
            "taklif": "Uyushma yig'ilishlari kunini oldindan e'lon qilinsa",
        }
    )
    _print_summary(survey)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
