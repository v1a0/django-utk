from typing import Mapping, Protocol, Type
from unittest import TestCase, skip
from unittest.mock import MagicMock

from django.db import models

from django_utk.tests import faker
from django_utk.tests.factories import Factory

small_int = faker.RandInt(2, 42)


class MockModelOptions(MagicMock):
    def __new__(cls, fields: Mapping[str, type], **kwargs):
        options = MagicMock()
        options.fields = fields
        return options


class MockModel(MagicMock):
    def __new__(cls, name: str, fields: Mapping[str, type], **kwargs):
        def model_call(**kwargs):
            mock_instance = super().__call__(**kwargs)

            for kw_name, kw_value in kwargs.items():
                setattr(mock_instance, kw_name, kw_value)

        model = MagicMock()
        model.__name__ = name
        model.__call__ = MockModel.__call__
        model._meta = MockModelOptions(fields)
        return model


class FactoryTestCase(TestCase):
    def assertFactoryWorks(self, factory: Type[Factory], model: MagicMock):
        instance = factory()

        model_calls = model.call_args_list
        kwargs = model_calls[0].kwargs

        self.assertEqual(len(model_calls), 1)

        self.assertEqual(
            factory._meta.fields_set.keys(),
            kwargs.keys(),
        )

        for kw_name, kw in kwargs.items():
            expected_kwarg_type = model._meta.fields[kw_name]
            self.assertIsInstance(kw, expected_kwarg_type)

    def test__init__const(self):
        Person = MockModel("Person", {"name": str, "age": int, "friends": list})

        person_name = "person-name"
        person_age = 33
        person_fiends = []  # haha

        class PersonFactory(Factory):
            name = person_name
            age = person_age
            friends = person_fiends

            class Meta:
                model = Person

        for i in range(small_int()):
            PersonFactory()

            model_calls = Person.call_args_list
            kwargs = model_calls[i].kwargs

            self.assertEqual(len(model_calls), i + 1)
            self.assertEqual(kwargs["name"], person_name)
            self.assertEqual(kwargs["age"], person_age)
            self.assertEqual(kwargs["friends"], person_fiends)
            self.assertEqual(
                len(kwargs),
                len([person_name, person_age, person_fiends]),
            )

    @skip("TODO: fix it later")
    def test__init__SubFactory(self):
        Skill = MockModel("Skill", {"name": str})
        Person = MockModel("Person", {"skill": Skill})

        class SkillFactory(Factory):
            name = "skill-name"

            class Meta:
                model = Skill

        class PersonFactory(Factory):
            skill = SkillFactory.sub_factory()

            class Meta:
                model = Person

        for i in range(small_int()):
            PersonFactory()

            model_calls = Person.call_args_list
            kwargs = model_calls[i].kwargs

            self.assertEqual(kwargs["skill"], "Skill")

    def test__init__Sequence(self):
        Person = MockModel("Person", {"name": str})
        person_name_suffix = "-person"

        class PersonFactory(Factory):
            name = faker.Sequence(lambda n: f"{n}{person_name_suffix}")

            class Meta:
                model = Person

        for i in range(small_int()):
            PersonFactory()

            model_calls = Person.call_args_list
            kwargs = model_calls[i].kwargs

            self.assertTrue(kwargs["name"].endswith(person_name_suffix))
            self.assertEqual(kwargs["name"], f"{i}{person_name_suffix}")

    def test__init__ForEach(self):
        Person = MockModel("Person", {"name": str})
        persons_amount = small_int()
        persons_names = [f"person-name-{i}" for i in range(persons_amount)]

        class PersonFactory(Factory):
            name = faker.ForEach(persons_names)

            class Meta:
                model = Person

        for i in range(persons_amount):
            PersonFactory()

            model_calls = Person.call_args_list
            kwargs = model_calls[i].kwargs

            self.assertEqual(kwargs["name"], persons_names[i])

        with self.assertRaises(StopIteration):
            PersonFactory()

    def test__init__RandData(self):
        Person = MockModel("Person", {"age": int, "weight": float, "name": str})

        class PersonFactory(Factory):
            age = faker.RandInt()
            weight = faker.RandFloat()
            name = faker.RandString()

            class Meta:
                model = Person

        for i in range(small_int()):
            PersonFactory()

            model_calls = Person.call_args_list
            kwargs = model_calls[i].kwargs

            self.assertLessEqual(kwargs["age"], faker.RandInt.MAX)
            self.assertGreaterEqual(kwargs["age"], faker.RandInt.MIN)

            self.assertLessEqual(kwargs["weight"], faker.RandFloat.MAX)
            self.assertGreaterEqual(kwargs["weight"], faker.RandFloat.MIN)
            self.assertGreater(len(kwargs["name"]), 0)
            self.assertTrue(
                all(letter in faker.RandString.ALPHABET for letter in kwargs["name"])
            )

    def test__init__Choice_and_Choices(self):
        Person = MockModel("Person", {"name": str, "friends": list})

        persons_amount = small_int()
        persons_names = [f"person-name-{i}" for i in range(persons_amount)]

        class PersonFactory(Factory):
            name = faker.RandChoice(persons_names)
            friends = faker.RandChoices(persons_names, k=small_int())

            class Meta:
                model = Person

        for i in range(small_int()):
            PersonFactory()

            model_calls = Person.call_args_list
            kwargs = model_calls[i].kwargs

            self.assertIn(kwargs["name"], persons_names)

            for friend_name in kwargs["friends"]:
                self.assertIn(friend_name, persons_names)
