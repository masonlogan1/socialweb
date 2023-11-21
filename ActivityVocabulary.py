"""
AUTHOR:     Mason Logan <PythonActivityStreams@masonlogan.com>
CREATED:    July 16, 2023
UPDATED:    July 16, 2023
Implements objects for working with ActivityStreams. Objects are intended to
be used as an alternative to working directly with JSON-LD data.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec
from validators import url

CONTEXT = "https://www.w3.org/ns/activitystreams"


class ActivityStreamsObject:
    """
    Base class for providing optional validation on all ActivityStreams fields.
    All fields mentioned in the vocabulary spec are inspected for
    type-correctness if strictness is enabled; will raise a ValueError for
    any incorrectly formatted fields
    """
    # NOTE: NOT CURRENTLY IMPLEMENTED! THIS IS PLANNING FOR FUTURE WORK!
    # THIS CLASS ISN'T USED BY ANYTHING AT ALL RIGHT NOW!
    # The eventual goal is to give all descendent classes a validator for
    # incoming field data; all fields have their types specified by the spec
    # so we know what basic checks to include
    __strict = False

    @classmethod
    def strict_init(cls):
        # sounds like an old british man. "bloody hell, bit strict innit?"
        cls.__strict = True

    @classmethod
    def nonstrict_init(cls):
        cls.__strict = False


# ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
#
#   The Base Types
#       The six foundational classes that all other vocabulary
#       objects are built from
#
#   ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//





# ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
#
#   The Activity Types
#       These classes describe things an Actor might do with Objects
#
#  ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//



# ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
#
#   The Actor Types
#       These classes describe the types of users and automated
#       processes that might be performing Actions on Objects
#
#  ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//



# ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
#
#   The Object/Link Types
#       These classes describe the types of Objects an Actor might
#       be performing some kind of Action on, and the conceptual
#       Links that bind Objects, Actors, and their interactions together
#
#  ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//

