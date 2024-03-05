"""
Classes and functions for managing a Zope Database Cluster. A cluster is a
collection of object databases that all store the same type of object and
provides CRUD functionality as well as index, caching, and search.

The cluster manager is responsible for ensuring an adequate number of nodes are
available, indexing objects across the cluster for easy lookup, and rapidly
recalling objects. The user or process using a cluster should not have to know
anything about the internal logic, only the standard methods used to get
details on what the cluster contains and how to create, update, and delete the
contents.
"""
class ClusterDb:
    """
    Data access and management object for an object database cluster
    """

# STEP 1: CRUD OPERATIONS
# TODO: Cluster MUST be able to store objects to nodes based on hash value
#   of object id

# TODO: Cluster MUST be able to retrieve objects from nodes based on hash
#   value of the object id

# TODO: Cluster MUST be able to update objects stored in nodes based on hash
#   value of the object id

# TODO: Cluster MUST be able to delete objects stored in nodes based on hash
#   value of the object id


# STEP 2: NODE MANAGEMENT
# TODO: Cluster MUST be able to dynamically create new nodes based on the
#   overall number of objects

# TODO: Cluster MUST be able to migrate existing nodes to new nodes

# TODO: Cluster MUST be able to validate that one set of nodes contains the
#   contents of another

# TODO: Cluster MUST be able to change primary object cluster if more than one
#   set of nodes is available

# TODO: Cluster MUST be able to update dependent objects to use different set
#   of nodes

# TODO: Cluster MUST be able to disable and enable automatic resizing


# STEP 3: INDEX, CACHE, AND SEARCH

# TODO: Cluster SHOULD be able to create indexes that make searching for
#   objects easier

# TODO: Cluster SHOULD be able to cache objects:
#   - CACHE results with a request-per-minute rate >= 1
#   - UNCACHE results unrequested for 15 minutes

# TODO: Cluster SHOULD be able to accept a query and return a TUPLE of objects
#   matching the query parameters
