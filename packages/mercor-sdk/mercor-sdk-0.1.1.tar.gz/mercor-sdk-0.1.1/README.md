# Mercor SDK

## Introduction

The Mercor software development kit is meant for users of the Mercor trading
API that wish to access it using the Python programming language. Using this
SDK will have the benefit of removing some of the boilerplate for calling the
different endpoints.

## Installation

```
python -m pip install mercor-sdk
```

## Usage

Importing the client and token:

``` python
from mercor_sdk.client import MercorClient
from mercor_sdk.tokens import CryptoToken
```

Instantiating the client:

``` python
client = MercorClient("<my_algorithm_address>", "<my_password>")
```

Viewing the current balance of the algorithm:

``` python
balance = client.balance()
print(balance.supply)
```

Placing a buy order:

``` python
trade = client.buy(slippage=0.05, relative_amount=0.5)
print(trade.transaction_hash)
```

Placing a sell order:

``` python
trade = client.sell(slippage=0.05, relative_amount=0.5)
print(trade.transaction_hash)
```

Retrieving the status of a buy or sell order:

``` python
status = client.status(transaction_hash=trade.transaction_hash.value)
print(status.message)
```

Accessing data from the ticker:

``` python
ticker = client.ticker_list()
print(ticker[CryptoToken.ETH])
```

Accessing data for a specific token from the ticker:

``` python
token = client.ticker(CryptoToken.ETH)
print(token.price)
```
