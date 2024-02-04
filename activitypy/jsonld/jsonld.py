"""
Tools for working with json-ld data
"""
import logging
from activitypy.jsonld.json_output import PropertyJsonGenerator
from activitypy.jsonld.json_input import PropertyJsonIntake

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PropertyJsonLD(PropertyJsonGenerator, PropertyJsonIntake):
    """
    Class for representing JSON-LD data. Utilizes @property objects for pulling
    instance data into JSON text representation
    """
    # overridable dict for mapping a transformation function to a property
    default_transforms = {}
    # overridable dict for mapping class types to a function for loading them
    # as objects
    type_constructor_map = {}

    def __init__(self, acontext):
        PropertyJsonGenerator.__init__(self, acontext)
        PropertyJsonIntake.__init__(self, acontext)

    def __str__(self):
        return self.json()


class ApplicationActivityJson(PropertyJsonLD):
    """
    Base class for representing application/activity+json type objects
    """

    def __init__(self, acontext):
        super().__init__(acontext=acontext)
