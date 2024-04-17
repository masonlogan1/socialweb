# citrine.storage
### Classes and functions for storing objects into the database

## Classes

### Collection
A ZODB-persistable object that provides a metadata object and offers the ability
to enforce capacity limits.

#### **insert ( self, key, value )**
Adds the value to the collection at the specified key
- key: a hashable value to be used to identify the object
- value: the pickleable value to be store

#### **update ( self, collection )**


#### **pop ( self, key, default=None )**


#### **popitem ( self )**


#### **setdefault ( self, key, default)**


#### **clear ( self )**


#### **keys ( self )**


#### **iterkeys ( self, min=None, max=None )**


#### **values ( self )**


#### **itervalues ( self, min=None, max=None )**


#### **items ( self )**


#### **iteritems ( self, min=None, max=None )**


#### **byValue ( self, min=None )**


#### **maxKey ( self, max=None )**


#### **minKey ( self, min=None )**

