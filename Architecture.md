# Architecture

## Layers

### Data

IBKR, Earnings, Macro, Forex, Universe, SQLite

### Infrastructure

Scheduler Priority Queue Rate Limiter Downloader Data Validation

### Processing

Macro -\> Asset -\> FX -\> Country -\> Industry -\> Trend -\>
Fundamental -\> Earnings -\> Portfolio -\> Rule -\> AI

### Presentation

Dashboard Telegram Reports Calendar

### Research

Backtest Strategy Builder Performance Tracking

## Design Rules

-   AI explains, Python calculates.
-   All scores are explainable.
-   Every strategy must be backtestable.
-   Every module is independently replaceable.
