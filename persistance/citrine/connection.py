"""
Classes and functions for managing a socialweb object database. The connection
object provides a standard set of functions for communicating with the object
clusters as well as initiating standard maintenance jobs, providing health
updates on various components, providing information about the types of objects
available in the database, and managing JsonLdEngine objects that are used to
identify the structure of various objects.

The connection object is structured in a way that allows for easy adaptation
into a networked server, and uses threading to shift as many routine processes
such as rerunning indexes on a schedule and orchestrating maintenance for the
connected clusters.
"""

# TODO: Define MUST/SHOULD requirements
