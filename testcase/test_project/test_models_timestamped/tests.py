from datetime import datetime
from unittest.mock import MagicMock, patch

from common.testcases.model_fields_testcase import ModelFieldsTestCase
from django.test import TestCase
from django.utils import timezone
from test_models_timestamped.models import TimeStampedNote

from django_utk.db.fields import CreatedAtField, UpdatedAtField

rand_text = lambda: str(datetime.now())
frozen_time_1 = timezone.now()
frozen_time_2 = timezone.now()


class TimeStampedModelTestCase(ModelFieldsTestCase, TestCase):
    model = TimeStampedNote
    required_fields = {
        "created_at": {**CreatedAtField._required_kwargs},
        "updated_at": {**UpdatedAtField._required_kwargs},
    }

    @patch("django.utils.timezone.now")
    def test__fields__created_at(self, mock_now: MagicMock):
        """
        Checking is created_at works correctly
        """
        mock_now.return_value = frozen_time_1

        note_1: TimeStampedNote = TimeStampedNote.objects.create(text=rand_text())
        self.assertEqual(note_1.created_at, frozen_time_1)

        note_2: TimeStampedNote = TimeStampedNote.objects.create(text=rand_text())
        self.assertEqual(note_2.created_at, frozen_time_1)

        mock_now.return_value = frozen_time_2

        note_1.text = rand_text()
        note_1.save()
        note_1.refresh_from_db()

        self.assertEqual(note_1.created_at, frozen_time_1)
        self.assertEqual(note_2.created_at, frozen_time_1)

    @patch("django.utils.timezone.now")
    def test__fields__updated_at(self, mock_now: MagicMock):
        """
        Checking is created_at works correctly
        """
        mock_now.return_value = frozen_time_1

        note: TimeStampedNote = TimeStampedNote.objects.create(text=rand_text())
        self.assertEqual(note.updated_at, frozen_time_1)

        mock_now.return_value = frozen_time_2

        note.text = rand_text()
        note.save()
        note.refresh_from_db()

        self.assertEqual(note.updated_at, frozen_time_2)
