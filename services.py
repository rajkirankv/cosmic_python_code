from __future__ import annotations

import model
from model import OrderLine, Batch
from repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def deallocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    # model should raise an exception if line is not found in any of the batches
    batchref = model.deallocate(line, batches)
    session.commit()
    return batchref


def add_batch(batchref, sku, qty, eta, repo: AbstractRepository, session):
    batch = Batch(batchref, sku, qty, eta)
    repo.add(batch)
    session.commit()
