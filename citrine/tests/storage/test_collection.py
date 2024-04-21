from unittest import TestCase, main

from citrine.storage import collection as container

from BTrees import _OOBTree
BTree = _OOBTree.BTree


class CollectionStorageTests(TestCase):
    """
    Tests for the Collection class that ensure it can save and load objects
    using the standard BTree methods
    """

    def test_iterkeys(self):
        """
        Tests that the Collection.iterkeys method will iterate over all keys,
        iterate over keys when a range is specified, and will ALWAYS ignore
        the "meta" key
        :return:
        """
        collection = container.Collection()

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(collection.iterkeys()), [])

        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        for key, value in zip(keys, values):
            BTree.insert(collection.tree, key, value)

        # check for all keys
        expected = keys
        out = list(collection.iterkeys())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for keys 1, 2, and 3
        expected = keys[1:4]
        out = list(collection.iterkeys(min=keys[1], max=keys[3]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for keys 0, 1, and 2
        expected = keys[:3]
        out = list(collection.iterkeys(max=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for keys 2, 3, and 4
        expected = keys[2:]
        out = list(collection.iterkeys(min=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_itervalues(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collection = container.Collection()

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(collection.itervalues()), [])

        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        for key, value in zip(keys, values):
            BTree.insert(collection.tree, key, value)

        # check for all values
        expected = values
        out = list(collection.itervalues())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 1, 2, and 3
        expected = values[1:4]
        out = list(collection.itervalues(min=keys[1], max=keys[3]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 0, 1, and 2
        expected = values[:3]
        out = list(collection.itervalues(max=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 2, 3, and 4
        expected = values[2:]
        out = list(collection.itervalues(min=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_iteritems(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collection = container.Collection()

        # check that we receive an iterable that produces nothing
        self.assertEqual(dict(collection.iteritems()), {})

        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = dict()
        for key, value in zip(keys, values):
            BTree.insert(collection.tree, key, value)
            items[key] = value

        # check for all five values
        expected = {k: v for k, v in items.items()}
        out = dict(collection.iteritems())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 1, 2, and 3
        expected = {k: v for k, v in items.items() if k in keys[1:4]}
        out = dict(collection.iteritems(min=keys[1], max=keys[3]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 0, 1, and 2
        expected = {k: v for k, v in items.items() if k in keys[:3]}
        out = dict(collection.iteritems(max=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 2, 3, and 4
        expected = {k: v for k, v in items.items() if k in keys[2:]}
        out = dict(collection.iteritems(min=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_keys(self):
        """
        Tests that the Collection.iterkeys method will iterate over all keys,
        iterate over keys when a range is specified, and will ALWAYS ignore
        the "meta" key
        :return:
        """
        collection = container.Collection()

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(collection.keys()), [])

        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        for key, value in zip(keys, values):
            BTree.insert(collection.tree, key, value)

        # check for all keys
        expected = keys
        out = list(collection.keys())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_values(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collection = container.Collection()

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(collection.values()), [])

        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        for key, value in zip(keys, values):
            BTree.insert(collection.tree, key, value)

        # check for all values
        expected = values
        out = list(collection.values())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_items(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collection = container.Collection()

        # check that we receive an iterable that produces nothing
        self.assertEqual(dict(collection.items()), {})

        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = dict()
        for key, value in zip(keys, values):
            BTree.insert(collection.tree, key, value)
            items[key] = value

        # check for all five values
        expected = {k: v for k, v in items.items()}
        out = dict(collection.items())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_insert(self):
        """
        Test that the implementation of ``insert`` in the Collection class works
        as intended.

        Tests that we can insert values, that we cannot exceed capacity in
        strict mode, that we can exceed capacity with strict mode off, and that
        attempting to insert a value for meta will raise an exception
        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in zip(keys, values):
            collection.insert(key, value)

        # test that everything we have inserted made its way into the collection
        for key, value in items.items():
            self.assertEqual(BTree.get(collection.tree, key), value)

        # test that when strict==True, we cannot exceed the capacity
        with self.assertRaises(container.CollectionCapacityError):
            collection.insert('key5', 'val5')

        # test that when strict==False, we can exceed the capacity
        collection.strict = False
        collection.insert('key5', 'val5')
        self.assertEqual(BTree.get(collection.tree, 'key5'), 'val5')

    def test_update(self):
        """
        Tests that the implementation of ``update`` in the Collection class
        works as intended.

        Tests that we can a dict of values, that we cannot exceed capacity in
        strict mode, that we can exceed capacity with strict mode off, that
        attempting to insert a value for meta will raise an exception, and that
        if an update fails the size or type checks nothing will be added
        """
        collection = container.Collection(max_size=10, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}

        # test that everything made its way into the collection
        collection.update(items)
        for key, value in items.items():
            self.assertEqual(BTree.get(collection.tree, key), value)

        # test that when strict==True, we cannot exceed the capacity
        too_many = {f'key{i}': f'val{i}' for i in range(5, 20)}
        with self.assertRaises(container.CollectionCapacityError):
            collection.update(too_many)

        # check that a failed update does not insert ANY of the keys, even if
        # there is enough room for some of them
        for key in too_many.keys():
            self.assertNotIn(key, collection.keys())

        # test that when strict==False, we can exceed the capacity
        collection.strict = False
        too_many = {f'key{i}': f'val{i}' for i in range(5, 20)}
        collection.update(too_many)
        for key, value in too_many.items():
            self.assertEqual(BTree.get(collection.tree, key), value)

    def test_get(self):
        """
        Tests that the implementation of ``get`` in the Collection class
        works as intended.

        Tests that we can get a value back by its key, that attempting to
        directly access the meta object will raise an exception, and that we
        can set a default value for when a key does not exist.
        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in zip(keys, values):
            collection.insert(key, value)

        # test that every item can be accessed via get
        for key, value in items.items():
            self.assertEqual(collection.get(key), value)

        # test that the default value will be returned if a key does not exist
        self.assertEqual(collection.get('keyNull', 'valNull'), 'valNull')

        # test that the default is ignored if the key DOES exist
        self.assertEqual(collection.get(keys[0], 'valNull'), values[0])

    def test_maxkey(self):
        """
        Tests that the implementation of ``maxkey`` in the Collection class
        works as intended.

        Tests that we can get the key with the highest value, that we can
        define a ceiling, and that the meta object will not ever be returned
        (even if no other keys exist)
        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}

        with self.assertRaises(ValueError):
            collection.maxKey()

        for key, value in zip(keys, values):
            collection.insert(key, value)

        # 'meta' is the highest actual key, but we should NOT see it
        # tests that the highest key from our inserted values appears
        self.assertEqual(collection.maxKey(), keys[4])
        # tests that a lower-value key is returned if we set a ceiling
        self.assertEqual(collection.maxKey(max=keys[3]), keys[3])

    def test_minKey(self):
        """
        Tests that the implementation of ``minkey`` in the Collection class
        works as intended.

        Tests that we can get the key with the highest value, that we can
        define a floor, and that the meta object will not ever be returned
        (even if no other keys exist)
        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}

        with self.assertRaises(ValueError):
            collection.minKey()

        for key, value in zip(keys, values):
            collection.insert(key, value)

        # 'meta' is the highest actual key, but we should NOT see it
        # tests that the highest key from our inserted values appears
        self.assertEqual(collection.minKey(), keys[0])
        # tests that a higher-value key is returned if we set a floor
        self.assertEqual(collection.minKey(min=keys[2]), keys[2])

    def test_pop(self):
        """
        Tests that the implementation of ``pop`` in the Collection class
        works as intended.

        Tests that pop returns the correct value, that the value is removed
        from the collection after, that the meta object cannot be popped, and
        that attempting to pop a nonexistent object will raise a KeyError.
        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in items.items():
            collection.insert(key, value)

        # test that we get the desired value for the key
        value = collection.pop(keys[2])
        self.assertEqual(value, values[2])

        # test that the key-value pair has disappeared from the collection
        self.assertNotIn(value, collection.values())
        self.assertNotIn(keys[2], collection.keys())

        # test that attempting to pop a nonexistent value will raise a KeyError
        with self.assertRaises(KeyError):
            collection.pop('nonexistent key')

        # test that default will be returned if popping a nonexistent key
        value = collection.pop('nonexistent key', 'default')
        self.assertEqual(value, 'default')

        # test that default will not be returned if popping an existent key
        value = collection.pop(keys[0], 'default')
        self.assertEqual(value, values[0])

    def test_popitem(self):
        """
        Tests that the implementation of ``pop`` in the Collection class
        works as intended.

        Tests that pop returns the correct value, that the value is removed
        from the collection after, that the meta object cannot be popped, and
        that attempting to pop a nonexistent object will raise a KeyError.
        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in items.items():
            collection.insert(key, value)

        # test that we get the desired value for the key
        key, value = collection.popitem()
        self.assertEqual(key, keys[0])
        self.assertEqual(value, values[0])

        # test that the key-value pair has disappeared from the collection
        self.assertNotIn(key, collection.keys())
        self.assertNotIn(value, collection.values())

    def test_setdefault(self):
        """

        :return:
        """
        collection = container.Collection(max_size=6, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in items.items():
            collection.insert(key, value)

        # test that the default is returned if the key does not exist
        value = collection.setdefault('key5', 'val5')
        self.assertEqual(value, 'val5')

        # test that the new value has been inserted
        self.assertEqual(collection.get('key5'), 'val5')

        # test that the key value is returned if the key does exist
        value = collection.setdefault(keys[0], 'val0-1')
        self.assertEqual(value, values[0])

        # test that the value was not changed
        self.assertEqual(collection.get(keys[0]), values[0])

    def test_byValue(self):
        """

        """
        collection = container.Collection(max_size=6, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in items.items():
            collection.insert(key, value)

        value_key = tuple((value, key) for key, value in items.items())

        # test that we get an iterable of value-key pairs
        expected = value_key[::-1]
        actual = tuple(collection.byValue())
        self.assertEqual(expected, actual)

        # test that meta never appears in any returns
        for value, key in expected:
            self.assertNotEqual(key, 'meta')

        # test that we get a list of value-key pairs where a minimum is set
        expected = value_key[2::-1]
        actual = tuple(collection.byValue(min='key2'))
        self.assertEqual(expected, actual[2:])

    def clear(self):
        """

        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in items.items():
            collection.insert(key, value)

        meta = collection.meta

        # test that all non-meta objects are removed
        collection.clear()
        self.assertEqual(collection.size, 0)
        for key, value in collection.items():
            self.assertNotIn(key, collection.keys())
            self.assertNotIn(value, collection.values())

        # test that meta remains completely intact
        self.assertEqual(meta, collection.meta)

    def has_key(self):
        """

        """
        collection = container.Collection(max_size=5, strict=True)
        keys = ['key0', 'key1', 'key2', 'key3', 'key4']
        values = ['val0', 'val1', 'val2', 'val3', 'val4']
        items = {key: value for key, value in zip(keys, values)}
        for key, value in items.items():
            collection.insert(key, value)

        # test that keys in the collection are all found
        for key in keys:
            self.assertTrue(collection.has_key(key))

        # test that keys not in the collection are not found
        for key in ['key5', 'key6', 'key7']:
            self.assertFalse(collection.has_key(key))

        # test that meta also shows as True
        self.assertTrue(collection.has_key('meta'))


if __name__ == '__main__':
    unittest.main()
