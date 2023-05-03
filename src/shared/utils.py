class Utils:
    @staticmethod
    def get_method_name(obj, func_name: str = "") -> str:
        obj_class_name = f"{obj.__class__.__module__}." \
                         f"{obj.__class__.__qualname__}"
        return f"{obj_class_name}.{func_name}" if func_name else obj_class_name

    @staticmethod
    def add_attributes(obj, data: dict) -> None:
        for key, value in data.items():
            setattr(obj, key, value)

    @staticmethod
    def discard_empty_attributes(obj) -> None:
        obj_copy = obj.__dict__.copy()
        for key, value in obj_copy.items():
            if not value:
                delattr(obj, key)

    @staticmethod
    def get_error_details(errors):
        return list(map(lambda error:
                        f"{error['loc'][1]}: {error['msg']} in {error['loc'][0]}"
                        if len(error['loc']) > 1 else f"{error['loc'][0]}: required", errors))
