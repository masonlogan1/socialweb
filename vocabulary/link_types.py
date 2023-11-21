"""
AUTHOR:     Mason Logan <PythonActivityStreams@masonlogan.com>
CREATED:    November 16, 2023
UPDATED:    November 16, 2023
Implements core objects for working with ActivityStreams. Objects are intended
to be used as an alternative to working directly with JSON-LD data.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec
from vocabulary import Link


class Mention(Link):
    """
    A specialized Link that represents an @mention.
    """
