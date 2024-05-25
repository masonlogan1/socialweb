"""
Classes for creating duplicates of classes and wrapping their methods/properties
in a way the ensures returned values are part of the same collection of classes.
Intended to be utilized by jsonld.package.JsonLdPackage
"""
import logging

from jsonld.utils import CLASS_CHANGE_CONTEXT


class ClassCloner:

    class DependencyNode:
        def __init__(self, cls, ref):
            self.cls = cls
            self.find_parents(ref)
            self.find_children(ref)

        def find_parents(self, ref):
            # anything in ref that is also a parent of cls
            candidates = [i for i in self.cls.mro()
                          if i in ref.keys() and self.cls != i]
            # filter out anything that is not a top-level dependency
            self.parents = {
                c: None
                for c in candidates
                if not any(c in i.mro() for i in candidates if c != i)
            }

        def find_children(self, ref):
            # anything in ref that is a child of cls
            candidates = [i for i in ref.keys()
                          if self.cls in i.mro() and self.cls != i]
            # filter out anything with dependencies other than self.cls
            self.children = {
                c: None
                for c in candidates
                if not any(
                    m for m in c.mro() if
                    self.cls != m and m in ref.keys() and c != m
                )
            }

        def set_nodes(self, ref):
            for key in self.parents.keys():
                self.parents[key] = ref.get(key, None)
            for key in self.children.keys():
                self.children[key] = ref.get(key, None)

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
        dep_tree = {cls: self.DependencyNode(cls, class_ref)
                    for cls in class_ref.keys()}
        for node in dep_tree.values():
            node.find_parents(dep_tree)
        for node in dep_tree.values():
            node.find_children(dep_tree)
        for node in dep_tree.values():
            node.set_nodes(dep_tree)

        ordered_nodes = list()
        while any(node not in ordered_nodes for node in dep_tree.values()):
            ordered_nodes += list(filter(
                lambda n: all(
                    parent in ordered_nodes for parent in n.parents.values()
                ) and n not in ordered_nodes, dep_tree.values()))

        for node in ordered_nodes:
            # IF there is a cloned class for a dependency (root will not have!)
            # THEN have the dependent cloned class inherit from it
            cls = node.cls
            inherits = [class_ref.get(p) for p in node.parents.keys()] + [cls]
            inherits = tuple(filter(lambda n: n is not None, inherits))

            class_ref[cls] = type(cls.__name__, inherits, cls.__dict__.copy())
            # change the return value for callables in class and properties
            self.wrap_callables(class_ref[cls])
            self.wrap_properties(class_ref[cls])
            # give cloned classes a reference back to their creator
            setattr(class_ref[cls], '__jsonld_package__', self)
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
            if callable(method) and not name.startswith('__'):
                setattr(cls, name, wrapper(method))

    def wrap_properties(self, cls):
        """
        Wraps the fget of a property with a function that changes the return
        value if the class of the return value is in the package
        """
        def get_wrapper(fn):
            def wrap_return(*args, **kwargs):
                if (val := fn(*args, **kwargs)).__class__ not in self.object_ref.keys():
                    return val
                with val.switch_context(CLASS_CHANGE_CONTEXT):
                    return self.change_class(val, self.object_ref.get(val.__class__))
            return wrap_return

        def set_wrapper(fn):
            def wrap_input(val, *args, **kwargs):
                if val.__class__ not in self.object_ref.keys():
                    fn(val, *args, **kwargs)
                    return
                with val.switch_context(CLASS_CHANGE_CONTEXT):
                    fn(self.change_class(val, self.object_ref.get(val.__class__)),
                       *args, **kwargs)
            return wrap_input

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
            wrapped = property(fget=get_wrapper(prop.fget),
                               fset=set_wrapper(prop.fset),
                               fdel=prop.fdel, doc=prop.__doc__)
            setattr(cls, name, wrapped)
