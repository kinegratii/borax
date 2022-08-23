__all__ = ['pll2cnl']


def _get(item, key):
    try:
        return getattr(item, key)
    except AttributeError:
        pass
    try:
        return item[key]
    except KeyError:
        pass
    raise ValueError(f'Item {item!r} has no attr or key for {key!r}')


def _parse_extra_data(item, *, flat_fields, extra_fields, extra_key, trs_fields=None):
    if isinstance(item, dict) and not flat_fields and not extra_key:
        trs_fields = trs_fields or []
        return {k: v for k, v in item.items() if k not in trs_fields}
    flat_data = {f: _get(item, f) for f in flat_fields}
    if extra_key:
        extra_data = {f: _get(item, f) for f in extra_fields}
        return {
            **flat_data,
            **{extra_key: extra_data}
        }
    return flat_data


def pll2cnl(
        nodelist,
        *,
        # source Data Settings
        id_field='id',
        parent_field='parent',
        root_value=None,
        # Generated Data Settings
        children_field='children',
        flat_fields=None,
        extra_fields=None,
        extra_key=None

):
    # Prepare and check params
    flat_fields = flat_fields or []
    extra_fields = extra_fields or []

    for f in flat_fields:
        if f in (id_field, parent_field, children_field):
            raise ValueError(f'Invalid field name: {f}')
    if extra_key and extra_key in (id_field, parent_field, children_field):
        raise ValueError('extra_key can not be empty when flat is set to False.')

    # Start build
    forest = []
    nodes = {}

    for item in nodelist:

        node_id = _get(item, id_field)
        parent_id = _get(item, parent_field)
        node = nodes.get(node_id, {id_field: node_id})
        kwargs_data = _parse_extra_data(
            item,
            flat_fields=flat_fields,
            extra_fields=extra_fields,
            extra_key=extra_key,
            trs_fields=(id_field, parent_field)
        )
        node.update(kwargs_data)
        nodes[node_id] = node

        if parent_id == root_value:
            # add node to forrest
            forest.append(node)
        else:
            # create parent node if necessary
            if parent_id in nodes:
                parent = nodes[parent_id]

            else:
                parent = {id_field: parent_id}
                nodes[parent_id] = parent
            # create children if necessary
            if children_field not in parent:
                parent[children_field] = []
            # add node to children of parent
            parent[children_field].append(node)

    return forest
