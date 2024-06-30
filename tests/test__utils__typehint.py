from unittest import TestCase
from unittest.mock import MagicMock

from django_utk.utils.typehint import typehint


class MockType:
    def __new__(cls) -> MagicMock:
        return MagicMock(spec=type)


class TypehintTestCase(TestCase):

    def assertAnnotations(self, method: any, annotations: dict):
        method_annotations = method.__annotations__

        self.assertListEqual(list(method_annotations.keys()), list(annotations.keys()))

        for annotation_name, annotation in annotations.items():
            self.assertIs(method_annotations[annotation_name], annotation)

    def assertClassAnnotations(self, klass: type, annotations: dict):
        for method_name, method_annotations in annotations.items():
            self.assertAnnotations(getattr(klass, method_name), method_annotations)

    def test__methods(self):
        method_a__return = MockType()
        method_b__return = MockType()
        method_c__return = MockType()
        method_d__return = MockType()
        method_e__return = MockType()
        method_f__return = MockType()

        arg_first__type = MockType()
        arg_second__type = MockType()
        arg_third__type = MockType()

        class ClassA:
            call_handler = MagicMock()
            call_handler.return_value = MagicMock()

            def method_a(self):
                return self.call_handler()

            def method_b(self, first):
                return self.call_handler(first=first)

            def method_c(self, first, second):
                return self.call_handler(first=first, second=second)

            def method_d(self, first, second, *, third):
                return self.call_handler(first=first, second=second, third=third)

            def method_e(self, *first, **second):
                return self.call_handler(first=first, second=second)

            @classmethod
            def method_f(cls):
                return cls.call_handler()

        class ClassB(ClassA):
            @typehint
            def method_a(
                self,
            ) -> method_a__return:
                pass

            @typehint
            def method_b(
                self,
                first: arg_first__type,
            ) -> method_b__return:
                pass

            @typehint
            def method_c(
                self,
                first: arg_first__type,
                second: arg_second__type,
            ) -> method_c__return:
                pass

            @typehint
            def method_d(
                self,
                first: arg_first__type,
                second: arg_second__type,
                *,
                third: arg_third__type,
            ) -> method_d__return:
                pass

            @typehint
            def method_e(
                self,
                *first: arg_first__type,
                **second: arg_second__type,
            ) -> method_e__return:
                pass

            @classmethod
            @typehint
            def method_f(
                cls,
            ) -> method_f__return:
                return cls.call_handler()

        class ClassC(ClassA):
            @typehint(ClassA)
            def method_a(
                self,
            ) -> method_a__return:
                pass

            @typehint(ClassA)
            def method_b(
                self,
                first: arg_first__type,
            ) -> method_b__return:
                pass

            @typehint(ClassA)
            def method_c(
                self,
                first: arg_first__type,
                second: arg_second__type,
            ) -> method_c__return:
                pass

            @typehint(ClassA)
            def method_d(
                self,
                first: arg_first__type,
                second: arg_second__type,
                *,
                third: arg_third__type,
            ) -> method_d__return:
                pass

            @typehint(ClassA)
            def method_e(
                self,
                *first: arg_first__type,
                **second: arg_second__type,
            ) -> method_e__return:
                pass

            @classmethod
            @typehint(ClassA)
            def method_f(
                cls,
            ) -> method_f__return:
                return cls.call_handler()

        annotations_mapping = {
            "method_a": {
                "return": method_a__return,
            },
            "method_b": {
                "first": arg_first__type,
                "return": method_b__return,
            },
            "method_c": {
                "first": arg_first__type,
                "second": arg_second__type,
                "return": method_c__return,
            },
            "method_d": {
                "first": arg_first__type,
                "second": arg_second__type,
                "third": arg_third__type,
                "return": method_d__return,
            },
            "method_e": {
                "first": arg_first__type,
                "second": arg_second__type,
                "return": method_e__return,
            },
            "method_f": {
                "return": method_f__return,
            },
        }

        self.assertClassAnnotations(klass=ClassB, annotations=annotations_mapping)
        self.assertClassAnnotations(klass=ClassC, annotations=annotations_mapping)

        original = ClassA()
        instance_b = ClassB()
        instance_c = ClassC()

        _first = MagicMock()
        _second = MagicMock()
        _third = MagicMock()

        instance_c.method_f()

        for instance in [instance_b, instance_c]:
            # method A
            self.assertIs(original.method_a(), instance.method_a())

            # method B
            self.assertIs(original.method_b(_first), instance.method_b(_first))
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)

            self.assertIs(
                original.method_b(first=_first),
                instance.method_b(first=_first),
            )
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)

            # method C
            self.assertIs(
                original.method_c(_first, _second),
                instance.method_c(_first, _second),
            )
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)
            self.assertIs(original.call_handler.call_args.kwargs["second"], _second)

            self.assertIs(
                original.method_c(_first, second=_second),
                instance.method_c(_first, second=_second),
            )
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)
            self.assertIs(original.call_handler.call_args.kwargs["second"], _second)

            self.assertIs(
                original.method_c(first=_first, second=_second),
                instance.method_c(first=_first, second=_second),
            )
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)
            self.assertIs(original.call_handler.call_args.kwargs["second"], _second)

            # method D
            self.assertIs(
                original.method_d(_first, _second, third=_third),
                instance.method_d(_first, _second, third=_third),
            )
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)
            self.assertIs(original.call_handler.call_args.kwargs["second"], _second)
            self.assertIs(original.call_handler.call_args.kwargs["third"], _third)

            self.assertIs(
                original.method_d(_first, second=_second, third=_third),
                instance.method_d(_first, second=_second, third=_third),
            )
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)
            self.assertIs(original.call_handler.call_args.kwargs["second"], _second)
            self.assertIs(original.call_handler.call_args.kwargs["third"], _third)

            self.assertIs(
                original.method_d(first=_first, second=_second, third=_third),
                instance.method_d(first=_first, second=_second, third=_third),
            )
            self.assertIs(original.call_handler.call_args.kwargs["first"], _first)
            self.assertIs(original.call_handler.call_args.kwargs["second"], _second)
            self.assertIs(original.call_handler.call_args.kwargs["third"], _third)

            # method E
            self.assertIs(
                original.method_e(_first, second=_second),
                instance.method_e(_first, second=_second),
            )
            self.assertTupleEqual(
                original.call_handler.call_args.kwargs["first"],
                (_first,),
            )
            self.assertDictEqual(
                original.call_handler.call_args.kwargs["second"],
                {"second": _second},
            )

            self.assertIs(
                original.method_e(_first, _first, second_1=_second, second_2=_second),
                instance.method_e(_first, _first, second_1=_second, second_2=_second),
            )
            self.assertTupleEqual(
                original.call_handler.call_args.kwargs["first"],
                (_first, _first),
            )
            self.assertDictEqual(
                original.call_handler.call_args.kwargs["second"],
                {"second_1": _second, "second_2": _second},
            )

            # method F
            self.assertIs(original.method_f(), instance.method_f())

    def test__magic(self):
        class ClassA:
            call_handler = MagicMock()
            call_handler__return = MagicMock()
            call_handler.return_value = call_handler__return

            def __new__(cls, *args, **kwargs):
                cls.call_handler(*args, **kwargs)
                return super().__new__(cls)

            def __init__(self, *args, **kwargs):
                self.call_handler(*args, **kwargs)

            def __call__(self, *args, **kwargs):
                return self.call_handler(*args, **kwargs)

        class ClassB(ClassA):
            @typehint
            def __new__(cls, *args, **kwargs):
                pass

            @typehint
            def __init__(self, *args, **kwargs):
                pass

            @typehint
            def __call__(self, *args, **kwargs):
                pass

        class ClassC(ClassA):
            @typehint(ClassA)
            def __new__(cls, *args, **kwargs):
                pass

            @typehint(ClassA)
            def __init__(self, *args, **kwargs):
                pass

            @typehint(ClassA)
            def __call__(self, *args, **kwargs):
                pass

        for Klass in [ClassB, ClassC]:
            data = MagicMock()
            instance = Klass(data=data)

            self.assertIsInstance(instance, Klass)
            self.assertIsInstance(instance, ClassA)

            for args in ClassA.call_handler.call_args_list[-2:]:
                # last two calls: init and new
                self.assertIs(args.kwargs["data"], data)
                self.assertIs(args.kwargs["data"], data)

            self.assertIs(instance(), ClassA.call_handler__return)
