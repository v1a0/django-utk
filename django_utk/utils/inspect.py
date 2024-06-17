def get_child_class_attrs(
    child_class: type,
    base_class: type,
    allowed_callable_types: tuple[type],
) -> dict:
    """
    Get all attributes of child-class that base-class doesn't have
    """

    def is_custom_attr(attr_name, attr_value):
        """Check is attribute custom field"""
        is_factory_class_attr = attr_name in base_class.__dict__
        is_method = callable(attr_value) and not isinstance(
            attr_value, allowed_callable_types
        )
        return not is_factory_class_attr and not is_method

    return {
        attr_name: attr_value
        for attr_name, attr_value in child_class.__dict__.items()
        if is_custom_attr(attr_name, attr_value)
    }
