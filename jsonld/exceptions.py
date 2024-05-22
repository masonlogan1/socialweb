class MissingContextError(Exception):
    """
    Exception thrown when attempting to access a ContextualProperty that has
    no contexts
    """
    def __init__(self, context=None, type=None, name=None):
        msg = ('ContextualProperty has no default' +
               (f" {type if type else ''}" if type is not None else "") +
               (f" for '{name}'" if name is not None else "") +
               (f" and is missing context '{context}'"
                if context is not None else ''))
        super().__init__(msg)
