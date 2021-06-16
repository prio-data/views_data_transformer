from typing import List, Optional
from collections import defaultdict
from . import exceptions

class TransformFunctionRegistry:
    """
    A registry containing transform functions that can be applied.
    """
    def __init__(self):
        self._functions = defaultdict(lambda: defaultdict(dict))

    def register_function(self,
            function,
            namespace: str,
            name: str,
            applicable_to: Optional[List[str]] = None):
        """
        Register the function in the internal data structure.
        """
        if applicable_to is None:
            applicable_to = ["any"]

        for data_type in applicable_to:
            self._functions[data_type][namespace][name] = function

    def register(self,
            namespace: str,
            name: str,
            applicable_to: Optional[List[str]] = None):
        """
        Function decorator that can be used to register a function, making it
        available as a transform.
        """
        def decorator(fn):
            self.register_function(fn, namespace, name, applicable_to)
            return fn
        return decorator

    def get_transform(self, data_type, namespace, name):
        """
        Retrieve a transform from the registry
        """
        try:
            return self._functions[data_type][namespace][name]
        except KeyError as ke:
            if data_type == "any":
                raise exceptions.NotRegistered(data_type,namespace,name) from ke
            return self.get_transform("any", namespace, name)

    def list_transforms(self):
        transforms = []
        for loa in self._functions.keys():
            for namespace in self._functions[loa]:
                for name in self._functions[loa][namespace]:
                    transforms.append({
                            "loa": loa,
                            "namespace": namespace,
                            "name": name,
                            "path_name": ".".join((namespace,name))
                        })
        return transforms
