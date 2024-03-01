# SocialWeb

SocialWeb is a project intended to provide processing tools for processing
social internet data as defined by the W3 Social Web specifications:

https://www.w3.org/TR/social-web-protocols/

The jsonld module provides a set of classes that can be used to build out
representations of Objects and Properties, a packaging system that can connect
them together, and an engine that can be used to process raw data into native
Python objects.

Additional tools and methods, such as tools for retrieving activitystreams and
jsonld data from online sources, are also provided.

The following specifications have out-of-the-box support: 

#### Activity Streams 2.0 Core
https://www.w3.org/TR/activitystreams-core/

#### ActivityPub (*in progress*)
https://www.w3.org/TR/activitypub/

## Quick Use Guide

### Creating an Engine

Out-of-the-box implementations come with a convenient create_engine method:
```python3
from activitystreams import create_engine

engine = create_engine()

# engines can directly create objects they are able to process
obj = engine.Object('https://example.org/obj/0')
print(obj.json(indent=2))
```
```
{
  "id": "https://example.org/obj/0",
  "@context": "https://www.w3.org/ns/activitystreams"
}
```

Engines also come with the ability to process raw json strings and convert them
into an object:
```python
from activitystreams import create_engine

engine = create_engine()

json_txt = '''{
    "id": "https://example.org/@user0",
    "type": "Person",
    "@context": "https://www.w3.org/ns/activitystreams"
}'''

user = engine.from_json(json_txt)

print(type(user))
```
```
<class 'activitystreams.models.Person'>
```

The social web is also capable of being traversed from a single entry point!
Links will automatically be opened as the next node on the social graph when
evaluated, when possible (if not possible, a Link object is presented):
```python
from activitystreams import create_engine
from jsonld import jsonld_get
engine = create_engine()

data = jsonld_get('https://gaygeek.social/users/engiqueering/outbox')
outbox = engine.from_json(data)

# might take a second, objects are requested from the web one at a time
last_post_timestamp = outbox.first.orderedItems[0].object.published
```
*(the result of that will be different based on when you run it, but it should
give you a datetime.datetime object)*
