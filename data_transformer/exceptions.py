
class NotRegistered(Exception):
    """
    Raised when attempting to apply a transform that is not registered
    """
    def __init__(self, data_type, namespace, name):
        message = (
                f"Transform {namespace}.{name} is not registered for {data_type}"
                )
        super().__init__(message)
