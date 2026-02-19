-- Table for Daily Data
CREATE TABLE IF NOT EXISTS stock_prices_1d (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(20, 4),
    close NUMERIC(20, 4),
    high NUMERIC(20, 4),
    low NUMERIC(20, 4),
    volume BIGINT,
    dividends NUMERIC(20, 4), 
    UNIQUE (symbol, date)
);

-- Table for Weekly Data
CREATE TABLE IF NOT EXISTS stock_prices_1wk (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(20, 4),
    close NUMERIC(20, 4),
    high NUMERIC(20, 4),
    low NUMERIC(20, 4),
    volume BIGINT,
    dividends NUMERIC(20, 4), 
    UNIQUE (symbol, date)
);

-- Table for Monthly Data
CREATE TABLE IF NOT EXISTS stock_prices_1mo (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(20, 4),
    close NUMERIC(20, 4),
    high NUMERIC(20, 4),
    low NUMERIC(20, 4),
    volume BIGINT,
    dividends NUMERIC(20, 4), 
    UNIQUE (symbol, date)
);