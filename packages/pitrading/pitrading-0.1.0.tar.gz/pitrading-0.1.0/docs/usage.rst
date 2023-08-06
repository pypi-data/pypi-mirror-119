=====
Usage
=====

To use saaltfiish_boilerplate in a project::

    import saaltfiish_boilerplate

Holidays Submodule Usage::

    from saaltfiish_boilerplate.holidays import Holidays
    # Get all holidays
    Holidays.get_holidays()

    # convert date string to datetime
    tm = "20210901"
    dt = Holidays.to_datetime(tm)

    # test if a datetime is a tradingday
    Holidays.tradingday(dt)

    # get previous / next tradingday
    Holidays.prev_tradingday(dt)
    Holidays.next_tradingday(dt)

Instrument Submodule Usage::

    from saaltfiish_boilerplate.instrument import Instrument

    # initialize an instrument object
    ins = Instrument("20210909", morning=True)
    ins = Instrument("20210908")

    # get contract mapping of an instrument instance
    ins.get_contract_mapping()
    
    # customize query and result
    ins.get_contract_mapping(tab='Options',
                             col=['code', 'type', 'strike', 'expiration'],
                             colnames=['cc', 'tt', 'ss', 'exp'])

    # get tradable codes of an instrument instance
    ins.get_tradable_contracts()
