"""
Classes for creating duplicates of classes and wrapping their methods/properties
in a way the ensures returned values are part of the same collection of classes.
Intended to be utilized by jsonld.package.JsonLdPackage
"""
import logging

from jsonld.utils import CLASS_CHANGE_CONTEXT


class ClassCloner:
    def clone_classes(self, classes):
        """
        Clones the base objects used to create the package. Copying the classes
        allows the base objects to remain unchanged (i.e. the original objects
        do not have their properties linked or functionality altered outside
        the package)
        :param classes:
        :return:
        """
        # creates a dictionary that organizes classes based on how many
        # package-internal dependencies they have
        ordered = {}
        for cls in classes:
            deps = [c for c in classes if c in cls.mro() and c != cls]
            ordered[len(deps)] = ordered.get(len(deps), []) + [cls]

        # creates a list where classes are sorted by their number of deps
        classes = []
        for val in sorted(ordered.keys()):
            classes += ordered[val]

        class_ref = {cls: None for cls in classes}

        for cls in classes:
            # IF there is a cloned class for a dependency (root will not have!)
            # THEN have the dependent cloned class inherit from it
            inherits = [val for obj, val in class_ref.items()
                        if obj in cls.mro() and val is not None]
            inherits = (cls,) if not inherits else (inherits[-1], cls)
            class_ref[cls] = type(cls.__name__, inherits, cls.__dict__.copy())
            # change the return value for callables in class and properties
            self.wrap_callables(class_ref[cls])
            self.wrap_properties(class_ref[cls])
        return class_ref

    def change_class(self, obj, new_class):
        # fetch the property values, if any, that are applicable; then
        # fetch the current property values, if any, so that if the new class
        # does not implement the same properties, the values will be transferred
        # to the new class as attributes to avoid data loss when handling
        # the same data in different packages
        props = {name: getattr(obj, name, None)
                 for name in getattr(new_class, '__properties__', ())}
        attrs = {name: getattr(obj, name, None)
                 for name in getattr(obj, '__properties__', ())}
        # merge both for simplicity and to avoid setting the same values twice
        data = {**props, **attrs}
        obj.__class__ = new_class
        obj.__properties__ = obj.__get_properties__(refresh=True)
        for name, val in data.items():
            try:
                setattr(obj, name, val)
            except AttributeError:
                self.logger.exception(f'Could not set {name}')
        return obj

    def wrap_callables(self, cls):
        """
        Wraps anything callable for a class with a function that changes the
        type of return values if the class of the value is in the package.
        """
        def wrapper(fn):
            def wrap_return(*args, **kwargs):
                if (val := fn(*args, **kwargs)).__class__ not in self.object_ref.keys():
                    return val
                with val.switch_context(CLASS_CHANGE_CONTEXT):
                    return self.change_class(val, self.object_ref.get(val.__class__))
            return wrap_return
        # locate anything callable and wrap it so output values will be mapped,
        # when applicable
        for name, method in cls.__dict__.items():
            if callable(method):
                setattr(cls, name, wrapper(method))

    def wrap_properties(self, cls):
        """
        Wraps the fget of a property with a function that changes the return
        value if the class of the return value is in the package
        """
        def wrapper(fn):
            def wrap_return(*args, **kwargs):
                if (val := fn(*args, **kwargs)).__class__ not in self.object_ref.keys():
                    return val
                with val.switch_context(CLASS_CHANGE_CONTEXT):
                    return self.change_class(val, self.object_ref.get(val.__class__))
            return wrap_return

        props = dict()
        # considers both PropertyAwareObject and JsonProperty objects
        if '__get_properties__' in dir(cls):
            props = {**props,
                     **{prop: getattr(cls, prop)
                        for prop in cls.__get_properties__(refresh=True)}}
        if '__get_property_name__' in dir(cls):
            props = {**props,
                     **{cls.__get_property_name__():
                            getattr(cls, cls.__get_property_name__())}}

        # does not change the underlying function; args and kwargs will go
        # through unaltered, but returned values will come back as the
        # expected type
        for name, prop in props.items():
            if not isinstance(prop, property):
                # failsafe in case something unexpected comes in!
                continue
            wrapped = property(fget=wrapper(prop.fget), fset=prop.fset,
                               fdel=prop.fdel, doc=prop.__doc__)
            setattr(cls, name, wrapped)