"""
Common classes and utilities used by the Citrine database
"""
import logging
import uuid
from uuid import uuid4
from datetime import datetime

from ZODB.Connection import Connection

from citrine.persistence import DbContainer, DbMetadata
from citrine.persistence import CitrineThreadTransactionManager, autocommit


class CitrineConnection(Connection):
    """
    Modified version of the ZODB.Connection.Connection class that adds a few
    utility methods and attributes for enhanced performance.

    ALL actions performed by a CitrineConnection are transactional by default,
    unless the object is being used as a context manager in which case
    the transaction will be committed on closure. To disable automatic
    transactions, set self.auto_transaction to False.
    """

    @property
    def container(self):
        return self.root.container

    @property
    def meta(self):
        return self.root.meta

    def __init__(self, db, cache_size=400, before=None, cache_size_bytes=0,
                 transaction_manager=None, **db_args):
        super().__init__(db=db, cache_size=cache_size, before=before,
                         cache_size_bytes=cache_size_bytes)
        self.transaction_manager = transaction_manager or \
                                   CitrineThreadTransactionManager()
        self.auto_transaction = True
        self.open(self.transaction_manager)

        self.logger = getattr(self, 'logger', logging.getLogger(__name__))
        self.__checks()

    def num_containers(self) -> int:
        return self.container.containers_size

    def expand_containers(self, num: int):
        """
        Add the specified number of sub-containers to the connection's main
        container
        :param num: number of containers to expand by
        :return:
        """
        with self:
            self.container.expand_size(self.num_containers() + num)

    @autocommit
    def create(self, id: str, obj):
        """
        Converts the object into a persistable format and stores it to the
        database
        :param id:
        :param obj:
        :return:
        """
        self.root.container.save(id=id, obj=obj)

    def read(self, id):
        """
        Retrieves the object from the database and returns it to its original
        format
        :param id:
        :return:
        """
        return self.root.container.get(id)

    @autocommit
    def update(self, id, obj: object):
        """
        Locates the object by the given id and updates it to the new object
        :param id:
        :param obj:
        :return:
        """
        self.root.container.save(id, obj)

    @autocommit
    def delete(self, id):
        """
        Locates the object by the given id and removes it from the database
        :param id:
        :return:
        """
        self.root.container.remove(id)

    def __getitem__(self, keys):
        """
        Shortcut for the read method that can return multiple entities
        """
        if isinstance(keys, slice):
            raise TypeError(f'{self.__class__} indices must be strings or '
                            'iterables of strings, not slice')
        if isinstance(keys, str):
            return self.read(keys)
        return [self.read(id) for id in keys]

    def __enter__(self):
        # TODO: temp measure, should probably create a distinct class for
        #   handling (and possibly logging!) transactions with unique uuid vals
        transaction_id = str(uuid.uuid4())
        setattr(self.transaction_manager, 'transaction_id', transaction_id)
        self.logger.info(f'BEGIN TRANSACTION {transaction_id}')
        self.auto_transaction = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        transaction_id = self.transaction_manager.transaction_id
        self.transaction_manager.commit()
        self.logger.info(f'END TRANSACTION {transaction_id}')
        self.auto_transaction = True

    def __checks(self):
        """
        Performs checks that objects necessary for the CitrineConnection to
        function are present, and attempts to create them if they are not
        :return:
        """
        if not hasattr(self.root, 'container'):
            logging.warning('MISSING CONTAINER OBJECT "root.container", ' +
                            'CREATING NEW')
            with self:
                self.root.container = DbContainer()

        if not hasattr(self.root, 'meta'):
            logging.warning('MISSING METADATA OBJECT "root.meta", ' +
                            'CREATING NEW')
            with self:
                self.root.meta = DbMetadata()
