"""
The tools in this module exist to serve as a set of standard utilities. The
primary use case for these is to simplify things when dealing with persistence;
many systems may have issues if complex logic is kept inside of properties
or external dependencies get involved.

If you're building a new package or extending an existing one, consider using
the tools provided here. There is no plan to remove or change the (intended)
functionality of the tools, making these functions dependable when loading a
persisted object into a class.
"""
from jsonld.tools.url import validate_url, validate_acct_or_email
from jsonld.tools.datetime import is_activity_datetime, datetime_str, \
    parse_activitystream_datetime, timedelta_str
from jsonld.tools.type import SetterValidator
from jsonld.tools.number import is_nonnegative
