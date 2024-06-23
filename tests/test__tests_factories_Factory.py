from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import MagicMock

from django_utk.tests import faker
from django_utk.tests.factories import Factory

small_int = faker.RandInt(2, 42)


class FactoryTestCase(TestCase):
    def test__init__simple(self):
        PersonModel = MagicMock()

        person_name = "Person Name"
        person_age = 33
        person_fiends = []  # haha

        class PersonFactory(Factory):
            name = person_name
            age = person_age
            friends = person_fiends

            class Meta:
                model = PersonModel

        for i in range(small_int()):
            person: PersonModel = PersonFactory()

            model_calls = PersonModel.call_args_list
            kwargs = model_calls[i].kwargs

            self.assertIsInstance(person, MagicMock)
            self.assertEqual(len(model_calls), i + 1)
            self.assertEqual(kwargs["name"], person_name)
            self.assertEqual(kwargs["age"], person_age)
            self.assertEqual(kwargs["friends"], person_fiends)
            self.assertEqual(
                len(kwargs) - 2,    # MagicMock's internal kwargs
                len([person_name, person_age, person_fiends]),
            )

    def test__init__sub_factory(self):
        @dataclass
        class SkillModel:
            name: str

            def save(self):
                pass

        @dataclass
        class PersonModel:
            skill: SkillModel

            def save(self):
                pass

        class SkillFactory(Factory):
            name = "Skill Name"

            class Meta:
                model = SkillModel
                fields = ["name"]

        class PersonFactory(Factory):
            skill = SkillFactory.sub_factory()

            class Meta:
                model = PersonModel
                fields = ["skill"]

        for i in range(small_int()):
            person = PersonFactory()

            self.assertIsInstance(person.skill, SkillModel)

