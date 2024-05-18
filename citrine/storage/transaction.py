import uuid
import logging

from transaction import ThreadTransactionManager as ZoThreadTransactionManager
from transaction import TransactionManager as ZoTransactionManager

class TransactionManager(ZoTransactionManager):
    """
    Single-threaded transaction manager for persisting objects to a Citrine
    Database.

    Builds on the existing ``transaction.TransactionManager`` by providing
    decorators that allow the manager to make individual methods transactional
    and the ability to give each transaction a unique UUID for logging any
    action carried out in a transaction
    """

    def __init__(self, explicit=False):
        super().__init__(explicit=explicit)
        self.autocommit = True
        self.logger = logging.getLogger('CTransManager')
        self.logger.setLevel(logging.INFO)

    def __enter__(self):
        self.transaction_uuid = uuid.uuid4()
        self.logger.info(f'START TRANSACTION {self.transaction_uuid}')
        self.autocommit = False
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.commit()
            self.logger.info(f'TRANSACTION {self.transaction_uuid} SUCCESSFUL')
        else:
            self.abort()
            self.logger.error(f'TRANSACTION {self.transaction_uuid} FAILED')
        self.autocommit = True
        self.transaction_uuid = None


class ThreadTransactionManager(ZoThreadTransactionManager):
    """
    Thread-local CitrineTransactionManager that creates a copy in the thread
    that this object is used in.
    """

    def __init__(self):
        super().__init__()
        self.autocommit = True
        self.logger = logging.getLogger('CTransManager')
        self.logger.setLevel(logging.INFO)

    def __enter__(self):
        self.transaction_uuid = uuid.uuid4()
        self.logger.info(f'START TRANSACTION {self.transaction_uuid}')
        self.autocommit = False
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.commit()
            self.logger.info(f'TRANSACTION {self.transaction_uuid} SUCCESSFUL')
        else:
            self.abort()
            self.logger.error(f'TRANSACTION {self.transaction_uuid} FAILED')
        self.autocommit = True
        self.transaction_uuid = None


def autocommit(fn):
    """
    Decorator designed to work with CitrineTransactionManager. Decorator will
    automatically commit so long as the transaction manager's autocommit
    attribute is set to True.
    :param fn:
    :return:
    """

    def decorator(obj, id, *args, **kwargs):
        tm = obj.transaction_manager
        if not tm.autocommit:
            if getattr(tm, 'transaction_uuid', None):
                tm.logger.info(f'{tm.transaction_uuid}: {fn.__name__} {id}')
            return fn(obj, id, *args, **kwargs)
        with tm:
            tm.logger.info(f'{tm.transaction_uuid}: {fn.__name__} {id}')
            return fn(obj, id, *args, **kwargs)

    return decorator