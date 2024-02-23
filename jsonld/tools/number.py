def is_nonnegative(val, prop='', **kwargs):
    if val is None:
        return
    if val < 0:
        raise ValueError(f'Property "{prop}" must be greater than 0; ' +
                         f'got {val}')