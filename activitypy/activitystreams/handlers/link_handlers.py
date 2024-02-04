"""
Classes and functions for working with URI/IRI data
"""
from activitypy.activitystreams.models import LinkModel
from activitypy.activitystreams.utils import validate_url

from activitypy.jsonld import ApplicationActivityJson
from activitypy.jsonld.utils import jsonld_get
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LinkHandler:
    """Class serving as a decorator that can convert strings into Links"""

    def expand_link(self, data, *args, **kwargs):
        # if LinkModel isn't registered or this isn't a Link, pass the data
        # without expanding
        if not isinstance(data, LinkModel):
            return data

        link = data.__dict__.get('_Href__href', '')
        # if we don't have an href, we can't expand; pass the data forward
        if not link:
            return data

        try:
            resp_data = jsonld_get(link)
        except Exception as e:
            # if we hit an error, pass the data through
            logger.info(f'Encountered an error expanding url {link}' +
                             f'\n{e}')
            return data

        try:
            new_obj = ApplicationActivityJson.from_json(resp_data)
        except Exception as e:
            # if we fail to form the new object, pass the data through
            logger.exception(f'Encountered an error forming object ' +
                             f'from {link}\n{e}')
            return data
        return new_obj

    def getter(self, get_func, *args, **kwargs):
        """
        Decorator for automatically expanding Link objects
        """
        def decorator(obj):
            return self.expand_link(get_func(obj))
        return decorator

    def href_only(self, get_func):
        """
        Decorator for getting only the href value back from a link
        :param get_func: getter function being decorated
        :return: the href of the link
        """
        def decorator(obj):
            val = get_func(obj)
            # if it's a single link, return the href
            if isinstance(val, LinkModel):
                return val.href
            # if it's a list, return either the href or the item (if no href)
            if isinstance(val, list):
                return [item.href if isinstance(item, LinkModel) else item
                        for item in val]
            # if we don't have a handler, just give back what we found
            return val
        return decorator

    def setter(self, set_prop, *args, **kwargs):
        """
        Decorator that allows the setter of a JsonProperty object to convert
        various data types into Link objects as a default
        """
        def create_link(v):
            # if it's a string, create a single link
            if isinstance(v, str) and validate_url(v):
                return Link(href=v)
            if isinstance(v, dict) and v.get('href', None) and validate_url(v.get('href', '')):
                return Link(**v)
            # if it's an iterable other than a string or dict, create many links
            if isinstance(v, (list, tuple, set)):
                return [create_link(item) for item in v]
            return v

        def linkify(obj, val):
            val = create_link(val)
            set_prop(obj, val)
        return linkify