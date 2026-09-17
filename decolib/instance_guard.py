from abc import ABC
from pathlib import Path
from typing import Callable, override, Any

def instance_guard(max_instances : int, is_singleton : bool) -> Callable:
    if is_singleton and max_instances > 1:
        raise TypeError(f"<{Path(__file__).name}>/[{type(instance_guard).__name__}:{instance_guard.__name__}] -> Target decorated with '@{instance_guard.__name__}' is now singleton, it cannot have more than 1 instance!!!")
    elif is_singleton:
        max_instances = 1

    def decorator(target : type) -> object:
        if isinstance(target,function):
            raise TypeError(f"<{Path(__file__).name}>/[{type(instance_guard).__name__}:{instance_guard.__name__}] -> Target decorated with '@{instance_guard.__name__}' must be class!!!'")

        class ProxyClass(ABC):
            _max_instance_count : int = max_instances
            _instance_count : int = 0

            def __new__(proxy_cls, *args : Any, **kwargs : Any) -> object: # noqa
                instance: type = target(*args, **kwargs)

                ProxyClass._instance_count += 1

                if ProxyClass._instance_count > ProxyClass._max_instance_count:
                    raise TypeError(f"<{Path(__file__).name}>/[{type(instance_guard).__name__}:{instance_guard.__name__}] -> Target decorated with '@{instance_guard.__name__}' cannot have more than {ProxyClass._max_instance_count} instances, not {ProxyClass._instance_count} instances!!!")
                else:
                    return instance

            @classmethod
            @override
            def __subclasshook__(cls, subclass : type) -> bool:
                if cls.__name__ == subclass.__name__:
                    return True

                return super().__subclasshook__(subclass)

            def __init_subclass__(cls, **kwargs) -> None:
                if is_singleton:
                    raise TypeError(f"<{Path(__file__).name}>/[{type(instance_guard).__name__}:{instance_guard.__name__}] -> Target decorated with '@{instance_guard.__name__}' cannot have subclasses when it is singleton!!!")


        ProxyClass.__name__ = target.__name__
        ProxyClass.__doc__ = target.__doc__

        return ProxyClass
    return decorator
