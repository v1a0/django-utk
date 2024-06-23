from django_utk.utils.args import EMPTY


def popattr(obj: object, attr_name: str, default: any = EMPTY):
    try:
        attr, _ = getattr(obj, attr_name), delattr(obj, attr_name)
    except AttributeError as exc:
        if default is EMPTY:
            raise exc
        attr = default

    return attr
