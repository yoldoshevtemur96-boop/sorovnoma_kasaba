import json
import tempfile
import unittest
from pathlib import Path

from sorovnoma.survey import (
    DuplicateQuestionError,
    InvalidAnswerError,
    Question,
    Survey,
    build_sample_survey,
)


class QuestionTests(unittest.TestCase):
    def test_open_question_validates_non_empty_text(self):
        question = Question(id="taklif", text="Taklifingiz?")
        self.assertTrue(question.is_open)
        self.assertTrue(question.validate("Yaxshi bo'lardi"))
        self.assertFalse(question.validate("   "))

    def test_closed_question_validates_known_option(self):
        question = Question(id="mamnuniyat", text="?", options=["Ha", "Yo'q"])
        self.assertFalse(question.is_open)
        self.assertTrue(question.validate("Ha"))
        self.assertFalse(question.validate("Balki"))


class SurveyTests(unittest.TestCase):
    def setUp(self):
        self.survey = Survey(title="Test so'rovnomasi")
        self.survey.add_question(Question(id="q1", text="Yoshingiz?", options=["18-25", "26-40"]))
        self.survey.add_question(Question(id="q2", text="Fikringiz?"))

    def test_add_duplicate_question_raises(self):
        with self.assertRaises(DuplicateQuestionError):
            self.survey.add_question(Question(id="q1", text="boshqa"))

    def test_submit_response_requires_all_answers(self):
        with self.assertRaises(InvalidAnswerError):
            self.survey.submit_response({"q1": "18-25"})

    def test_submit_response_validates_options(self):
        with self.assertRaises(InvalidAnswerError):
            self.survey.submit_response({"q1": "noto'g'ri", "q2": "matn"})

    def test_submit_and_tally(self):
        self.survey.submit_response({"q1": "18-25", "q2": "yaxshi"})
        self.survey.submit_response({"q1": "18-25", "q2": "yomon"})
        self.survey.submit_response({"q1": "26-40", "q2": "o'rtacha"})

        self.assertEqual(self.survey.response_count(), 3)
        tally = self.survey.tally("q1")
        self.assertEqual(tally["18-25"], 2)
        self.assertEqual(tally["26-40"], 1)

    def test_save_and_load_round_trip(self):
        self.survey.submit_response({"q1": "18-25", "q2": "yaxshi"})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "survey.json"
            self.survey.save(path)

            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["title"], "Test so'rovnomasi")

            loaded = Survey.load(path)
            self.assertEqual(loaded.title, self.survey.title)
            self.assertEqual(loaded.response_count(), 1)
            self.assertEqual(loaded.tally("q1")["18-25"], 1)


class SampleSurveyTests(unittest.TestCase):
    def test_build_sample_survey_has_expected_questions(self):
        survey = build_sample_survey()
        ids = {q.id for q in survey.questions}
        self.assertEqual(ids, {"mamnuniyat", "tadbir", "taklif"})


if __name__ == "__main__":
    unittest.main()
