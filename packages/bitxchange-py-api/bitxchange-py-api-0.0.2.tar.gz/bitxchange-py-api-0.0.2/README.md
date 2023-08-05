# Bitxchange Python API Library
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/bitxchange-python-api/badge/?version=latest)](https://bitxchange-python-api.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://app.travis-ci.com/Wozinga/bitxchange_python_api.svg?branch=master)](https://app.travis-ci.com/Wozinga/bitxchange_python_api)
[![codecov](https://codecov.io/gh/Wozinga/bitxchange_python_api/branch/master/graph/badge.svg?token=V9JR3JRFEN)](https://codecov.io/gh/Wozinga/bitxchange_python_api)

This is a lightweight library that works as a connector to [Bitxchange public API](https://bitxchange-python-api.readthedocs.io/en/latest/)


## Installation
```bash
pip install bitxchange-py-api
```

## Documentation
https://bitxchange-python-api.readthedocs.io/en/latest/

## RESTful APIs
Usage examples:
```python
from bitxchange.spot import Spot

exchange = Spot(key='<api_key ', secret='api_secret')

params = {
    "amount": 1,
    "price": 0.05917959,
    "pair": "BTC/ETH",
    "order_type": 2,
    "type": "sell"
}

order = exchange.create_order(**params)

print(order)
```
You can find more examples in the documentation at the link above.
