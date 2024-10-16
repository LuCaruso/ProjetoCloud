import yfinance as yf

def get_stock_price(company: str):
    # Obtemos o ticker da ação
    ticker = yf.Ticker(company)
    
    # Obtendo o histórico de preços
    history = ticker.history(period="1d")
    if history.empty:
        return None
    
    # Recuperando o preço de fechamento
    closing_price = history['Close'][0]
    
    # Recuperando informações financeiras
    info = ticker.info

    #Extraindo nome da empresa
    company_name = info.get('longName', None)
    
    # Extraindo indicadores financeiros
    pe_ratio = info.get('forwardPE', None)  # Preço/Lucro
    dividend_yield = info.get('dividendYield', None)  # Dividend Yield
    market_cap = info.get('marketCap', None)  # Capitalização de mercado
    roe = info.get('returnOnEquity', None)  # Retorno sobre o patrimônio líquido

    return {
        "company_name": company_name,
        "closing_price": closing_price,
        "pe_ratio": pe_ratio,
        "dividend_yield": dividend_yield,
        "market_cap": market_cap,
        "roe": roe
    }
