from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import MagicMock

from django_utk.tests import faker
from django_utk.tests.factories import Factory
from django_utk.utils.typehint import typehint

small_int = faker.RandInt(2, 42)


class FactoryTestCase(TestCase):
    def test__init__const(self):
        PersonModel = MagicMock()

        person_name = "person-name"
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
                len(kwargs),
                len([person_name, person_age, person_fiends]),
            )

    def test__init__SubFactory(self):
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
            name = "skill-name"

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

    def test__init__Sequence(self):
        person_name_suffix = "-person"

        @dataclass
        class PersonModel:
            name: str

            def save(self):
                pass

        class PersonFactory(Factory):
            name = faker.Sequence(lambda n: f"{n}{person_name_suffix}")

            @typehint
            def __new__(cls, *args, **kwargs) -> PersonModel:
                pass

            class Meta:
                model = PersonModel
                fields = ["name"]

        for i in range(small_int()):
            person = PersonFactory()

            self.assertTrue(person.name.endswith(person_name_suffix))
            self.assertEqual(person.name, f"{i}{person_name_suffix}")

    def test__init__ForEach(self):
        persons_amount = small_int()
        persons_names = [f"person-name-{i}" for i in range(persons_amount)]

        @dataclass
        class PersonModel:
            name: str

            def save(self):
                pass

        class PersonFactory(Factory):
            name = faker.ForEach(persons_names)

            @typehint
            def __new__(cls, *args, **kwargs) -> PersonModel:
                pass

            class Meta:
                model = PersonModel
                fields = ["name"]

        for i in range(persons_amount):
            person = PersonFactory()

            self.assertEqual(person.name, persons_names[i])

        with self.assertRaises(StopIteration):
            PersonFactory()

    def test__init__RandData(self):
        @dataclass
        class PersonModel:
            age: int
            weight: float
            name: str

            def save(self):
                pass

        class PersonFactory(Factory):
            age = faker.RandInt()
            weight = faker.RandFloat()
            name = faker.RandString()

            @typehint
            def __new__(cls, *args, **kwargs) -> PersonModel:
                pass

            class Meta:
                model = PersonModel
                fields = ["age", "weight", "name"]

        for i in range(small_int()):
            person = PersonFactory()

            self.assertLessEqual(person.age, faker.RandInt.MAX)
            self.assertGreaterEqual(person.age, faker.RandInt.MIN)

            self.assertLessEqual(person.weight, faker.RandFloat.MAX)
            self.assertGreaterEqual(person.weight, faker.RandFloat.MIN)
            self.assertGreater(len(person.name), 0)
            self.assertTrue(
                all(letter in faker.RandString.ALPHABET for letter in person.name)
            )

    def test__init__Choice_and_Choices(self):
        persons_amount = small_int()
        persons_names = [f"person-name-{i}" for i in range(persons_amount)]

        @dataclass
        class PersonModel:
            name: str
            friends: list[str]

            def save(self):
                pass

        class PersonFactory(Factory):
            name = faker.RandChoice(persons_names)
            friends = faker.RandChoices(persons_names, k=small_int())

            @typehint
            def __new__(cls, *args, **kwargs) -> PersonModel:
                pass

            class Meta:
                model = PersonModel
                fields = ["name", "friends"]

        for i in range(small_int()):
            person = PersonFactory()

            self.assertIn(person.name, persons_names)

            for friend_name in person.friends:
                self.assertIn(friend_name, persons_names)
