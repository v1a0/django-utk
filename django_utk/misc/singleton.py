INSTANCE_KEY = "__instance__"


def get_instance(cls: type, getter: callable, key: str = INSTANCE_KEY):
    instance = getattr(cls, key, None) or getter(cls)
    setattr(cls, key, instance)
    return instance


class SingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        return get_instance(
            cls,
            lambda kls: super(SingletonMeta, kls).__call__(*args, **kwargs),
        )


class Singleton(metaclass=SingletonMeta):
    pass
