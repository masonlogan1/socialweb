from jsonld import (ApplicationActivityJson, JsonProperty, JsonLdPackage,
                    contextualproperty)


TEST_NAMESPACE = 'https://citrine.tools/ns/testurl'


class Pkg0TestObjectClass0(ApplicationActivityJson):
    """"""
    ___type___ = "Package0Class0"

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{TEST_NAMESPACE}#{cls.___type___}'


class Pkg0TestObjectClass1(ApplicationActivityJson):
    """"""
    ___type___ = "Package0Class1"

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{TEST_NAMESPACE}#{cls.___type___}'


class Pkg0TestObjectClass2(ApplicationActivityJson):
    """"""
    ___type___ = "Package0Class2"

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{TEST_NAMESPACE}#{cls.___type___}'


class Pkg1TestObjectClass0(ApplicationActivityJson):
    """"""
    ___type___ = "Package1Class0"

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{TEST_NAMESPACE}#{cls.___type___}'



class Pkg1TestObjectClass1(ApplicationActivityJson):
    """"""
    ___type___ = "Package1Class1"

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{TEST_NAMESPACE}#{cls.___type___}'


class Pkg1TestObjectClass2(ApplicationActivityJson):
    """"""
    ___type___ = "Package1Class2"

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{TEST_NAMESPACE}#{cls.___type___}'


class PropBase(JsonProperty):
    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{TEST_NAMESPACE}#dfn-{cls.__get_property_name__()}'


class Pkg0Obj0Prop0(PropBase):
    @contextualproperty
    def pkg0obj0prop0(self):
        return getattr(self, '_pkg0obj0prop0')

    @pkg0obj0prop0.setter
    def pkg0obj0prop0(self, value):
        setattr(self, '_pkg0obj0prop0', value)


class Pkg0Obj0Prop1(PropBase):
    @contextualproperty
    def pkg0obj0prop1(self):
        return getattr(self, '_pkg0obj0prop1')

    @pkg0obj0prop1.setter
    def pkg0obj0prop1(self, value):
        setattr(self, '_pkg0obj0prop1', value)


class Pkg0Obj0Prop2(PropBase):
    @contextualproperty
    def pkg0obj0prop2(self):
        return getattr(self, '_pkg0obj0prop2')

    @pkg0obj0prop2.setter
    def pkg0obj0prop2(self, value):
        setattr(self, '_pkg0obj0prop2', value)


class Pkg0Obj1Prop0(PropBase):
    @contextualproperty
    def pkg0obj1prop0(self):
        return getattr(self, '_pkg0obj1prop0')

    @pkg0obj1prop0.setter
    def pkg0obj1prop0(self, value):
        setattr(self, '_pkg0obj1prop0', value)


class Pkg0Obj1Prop1(PropBase):
    @contextualproperty
    def pkg0obj1prop1(self):
        return getattr(self, '_pkg0obj1prop1')

    @pkg0obj1prop1.setter
    def pkg0obj1prop1(self, value):
        setattr(self, '_pkg0obj1prop1', value)


class Pkg0Obj1Prop2(PropBase):
    @contextualproperty
    def pkg0obj1prop2(self):
        return getattr(self, '_pkg0obj1prop2')

    @pkg0obj1prop2.setter
    def pkg0obj1prop2(self, value):
        setattr(self, '_pkg0obj1prop2', value)


class Pkg0Obj2Prop0(PropBase):
    @contextualproperty
    def pkg0obj2prop0(self):
        return getattr(self, '_pkg0obj2prop0')

    @pkg0obj2prop0.setter
    def pkg0obj2prop0(self, value):
        setattr(self, '_pkg0obj2prop0', value)


class Pkg0Obj2Prop1(PropBase):
    @contextualproperty
    def pkg0obj2prop1(self):
        return getattr(self, '_pkg0obj2prop1')

    @pkg0obj2prop1.setter
    def pkg0obj2prop1(self, value):
        setattr(self, '_pkg0obj2prop1', value)


class Pkg0Obj2Prop2(PropBase):
    @contextualproperty
    def pkg0obj2prop2(self):
        return getattr(self, '_pkg0obj2prop2')

    @pkg0obj2prop2.setter
    def pkg0obj2prop2(self, value):
        setattr(self, '_pkg0obj2prop2', value)


class Pkg1Obj0Prop0(PropBase):
    @contextualproperty
    def pkg1obj0prop0(self):
        return getattr(self, '_pkg1obj0prop0')

    @pkg1obj0prop0.setter
    def pkg1obj0prop0(self, value):
        setattr(self, '_pkg1obj0prop0', value)


class Pkg1Obj0Prop1(PropBase):
    @contextualproperty
    def pkg1obj0prop1(self):
        return getattr(self, '_pkg1obj0prop1')

    @pkg1obj0prop1.setter
    def pkg1obj0prop1(self, value):
        setattr(self, '_pkg1obj0prop1', value)


class Pkg1Obj0Prop2(PropBase):
    @contextualproperty
    def pkg1obj0prop2(self):
        return getattr(self, '_pkg1obj0prop2')

    @pkg1obj0prop2.setter
    def pkg1obj0prop2(self, value):
        setattr(self, '_pkg1obj0prop2', value)


class Pkg1Obj1Prop0(PropBase):
    @contextualproperty
    def pkg1obj1prop0(self):
        return getattr(self, '_pkg1obj1prop0')

    @pkg1obj1prop0.setter
    def pkg1obj1prop0(self, value):
        setattr(self, '_pkg1obj1prop0', value)


class Pkg1Obj1Prop1(PropBase):
    @contextualproperty
    def pkg1obj1prop1(self):
        return getattr(self, '_pkg1obj1prop1')

    @pkg1obj1prop1.setter
    def pkg1obj1prop1(self, value):
        setattr(self, '_pkg1obj1prop1', value)


class Pkg1Obj1Prop2(PropBase):
    @contextualproperty
    def pkg1obj1prop2(self):
        return getattr(self, '_pkg1obj1prop2')

    @pkg1obj1prop2.setter
    def pkg1obj1prop2(self, value):
        setattr(self, '_pkg1obj1prop2', value)


class Pkg1Obj2Prop0(PropBase):
    @contextualproperty
    def pkg1obj2prop0(self):
        return getattr(self, '_pkg1obj2prop0')

    @pkg1obj2prop0.setter
    def pkg1obj2prop0(self, value):
        setattr(self, '_pkg1obj2prop0', value)


class Pkg1Obj2Prop1(PropBase):
    @contextualproperty
    def pkg1obj2prop1(self):
        return getattr(self, '_pkg1obj2prop1')

    @pkg1obj2prop1.setter
    def pkg1obj2prop1(self, value):
        setattr(self, '_pkg1obj2prop1', value)


class Pkg1Obj2Prop2(PropBase):
    @contextualproperty
    def pkg1obj2prop2(self):
        return getattr(self, '_pkg1obj2prop2')

    @pkg1obj2prop2.setter
    def pkg1obj2prop2(self, value):
        setattr(self, '_pkg1obj2prop2', value)


props = [Pkg0Obj0Prop0, Pkg0Obj0Prop1, Pkg0Obj0Prop2,
         Pkg0Obj1Prop0, Pkg0Obj1Prop1, Pkg0Obj1Prop2,
         Pkg0Obj2Prop0, Pkg0Obj2Prop1, Pkg0Obj2Prop2,
         Pkg1Obj0Prop0, Pkg1Obj0Prop1, Pkg1Obj0Prop2,
         Pkg1Obj1Prop0, Pkg1Obj1Prop1, Pkg1Obj1Prop2,
         Pkg1Obj2Prop0, Pkg1Obj2Prop1, Pkg1Obj2Prop2,]

objs = [Pkg0TestObjectClass0, Pkg0TestObjectClass1, Pkg0TestObjectClass2,
        Pkg1TestObjectClass0, Pkg1TestObjectClass1, Pkg1TestObjectClass2,]

mapping = {
    Pkg0TestObjectClass0.__get_namespace__(): (
        Pkg0Obj0Prop0.__get_namespace__(),
        Pkg0Obj0Prop1.__get_namespace__(),
        Pkg0Obj0Prop2.__get_namespace__()
    ),
    Pkg0TestObjectClass1.__get_namespace__(): (
        Pkg0Obj1Prop0.__get_namespace__(),
        Pkg0Obj1Prop1.__get_namespace__(),
        Pkg0Obj1Prop2.__get_namespace__()
    ),
    Pkg0TestObjectClass2.__get_namespace__(): (
        Pkg0Obj2Prop0.__get_namespace__(),
        Pkg0Obj2Prop1.__get_namespace__(),
        Pkg0Obj2Prop2.__get_namespace__()),
    Pkg1TestObjectClass0.__get_namespace__(): (
        Pkg1Obj0Prop0.__get_namespace__(),
        Pkg1Obj0Prop1.__get_namespace__(),
        Pkg1Obj0Prop2.__get_namespace__()
    ),
    Pkg1TestObjectClass1.__get_namespace__(): (
        Pkg1Obj1Prop0.__get_namespace__(),
        Pkg1Obj1Prop1.__get_namespace__(),
        Pkg1Obj1Prop2.__get_namespace__()
    ),
    Pkg1TestObjectClass2.__get_namespace__(): (
        Pkg1Obj2Prop0.__get_namespace__(),
        Pkg1Obj2Prop1.__get_namespace__(),
        Pkg1Obj2Prop2.__get_namespace__()),
}


def get_test_package():
    return JsonLdPackage(namespace=TEST_NAMESPACE,
                         objects=objs,
                         properties=props,
                         property_mapping=mapping)
