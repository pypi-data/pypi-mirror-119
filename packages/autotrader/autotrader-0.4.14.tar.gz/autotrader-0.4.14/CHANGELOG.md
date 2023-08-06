# AutoTrader Changelog

## Version 0.4.0
- Livetrade mode now supports bot detachment, so that bots will trade until
  a termination signal is received. This is achieved through the bot manager.
- Data time alginment can optionally be disabled
- Various plotting improvements

### 0.4.14
- Ability to suspend bots and stream when livetrading. This is useful for 
  weekends / closed trading period, where trading is not possible, but you
  do not wish to kill an active bot.
- Various stream connection improvements
- Docstring improvements

### 0.4.13
- Added 3 second sleep when reconnecting to Oanda API

### 0.4.12
- fix typo in connection check

### 0.4.11
- Added connection check to Oanda module


### 0.4.10
- Major improvements to AutoStream
- Livetrade with data updates directly from stream
- If running in detached bot mode, must include initialise_strategy(data)
method in strategy module so that it can recieve data updates from the bot
- Must also have exit_strategy(i) method in strategy module, to allow safe
strategy termination from bot manager
