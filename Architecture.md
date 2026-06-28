# Architecture

## Layers

### Data

-   IBKR
-   Market Data
-   Financial Data
-   Earnings
-   Macro
-   Forex
-   SQLite

### Processing

Macro → Asset → FX → Country → Industry → Trend → Fundamental → Earnings
→ Portfolio → Rule → AI

### Presentation

Dashboard Telegram Reports Calendar

### Research

Backtest Strategy Builder Optimization Performance

## Scheduler

All broker requests go through Scheduler + Queue + RateLimiter.

## Design Principles

-   Python calculates
-   AI explains
-   Every score is backtestable
-   Every module is replaceable
