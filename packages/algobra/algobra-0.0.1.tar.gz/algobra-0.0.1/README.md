# ALGOBRA

This is an algorithmic trading engine used to backtest, model, and develop trading strategies on real time/historic stock data.

## Installation
Run the following to install:
```python
pip install algobra
```

## Usage
```python
from algobra import engine

# Systems check to see if your machine can utilitize native performance improvements.
engine.optimize()

# See engine information
print(engine.info())
```

# Developing Algobra
To install algobra, along with the tools you need to develop and run tests, run the following in your virtualenv.

```bash
pip install -e .[dev]
```

## Concepts
- Trading System Development
- Trading System Design
- Trading System Environment
- Time Series Analysis
- Optimization
- Performance Measurements
- Risk Management
- Trading Strategy Implementation
- Execution

## Configuring DB

> mysql -u root -p

```
mysql> CREATE DATABASE securities_master;
mysql> USE securities_master;
mysql> CREATE USER ’sec_user’@’localhost’ IDENTIFIED BY ’password’;
mysql> GRANT ALL PRIVILEGES ON securities_master.* TO ’sec_user’@’localhost’;
mysql> FLUSH PRIVILEGES;
```

Reference `schemas.sql` for the commands to create needed tables