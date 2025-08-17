# Known converter currency IDs (multi-currency baskets from real blockchain data)
# These are converters that contain multiple reserve currencies
converter_ids = [
    "iHnYAmrS45Hb8GVgyzy7nVQtZ5vttJ9N3X",  # SUPERVRSC
    "iFrFn9b6ctse7XBzcWkRbpYMAHoKjbYKqG",  # SUPER🛒
    "i4Xr5TAMrDTD99H69EemhjDxJ4ktNskUtc",  # Switch
    "i9kVWKU2VwARALpbXn4RS9zvrhvNRaUibb",  # Kaiju
    "iH37kRsdfoHtHK5TottP1Yfq8hBSHz9btw",  # NATI🦉
    "iHax5qYQGbcMGqJKKrPorpzUBX2oFFXGnY",  # Pure
    "iAik7rePReFq2t7LZMZhHCJ52fT5pisJ5C",  # vYIELD
    "i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx",  # Bridge.vETH
    "iG1jouaqSJayNb9LCqPzb3yFYD3kUpY2P2",  # whales
    "iRt7tpLewArQnRddBVFARGKJStK6w5pDmC",  # NATI
]

# Excluded chains - these converters should not appear in API output
# Filtering is done by ticker name, not currency ID
excluded_chains = ["Bridge.CHIPS", "Bridge.vDEX", "Bridge.vARRR", "whales"]

# Complete currency mapping for all Verus currencies
# Includes both currencies with Ethereum contract addresses and native Verus currencies
currency_contract_mapping = {
    # Currencies with Ethereum contract addresses
    "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM": {
        "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "eth_symbol": "DAI",
        "vrsc_symbol": "DAI.vETH"
    },  # DAI.vETH
    "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE": {
        "address": "0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c",
        "eth_symbol": "EURC",
        "vrsc_symbol": "EURC.vETH"
    },  # EURC.vETH
    "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4": {
        "address": "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2",
        "eth_symbol": "MKR",
        "vrsc_symbol": "MKR.vETH"
    },  # MKR.vETH
    "iL62spNN42Vqdxh8H5nrfNe8d6Amsnfkdx": {
        "address": "0x4f14E88B5037F0cA24348Fa707E4A7Ee5318d9d5",
        "eth_symbol": "NATION",
        "vrsc_symbol": "NATI.vETH"
    },  # NATI.vETH
    "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV": {
        "address": "0xBc2738BA63882891094C99E59a02141Ca1A1C36a",
        "eth_symbol": "VRSC",
        "vrsc_symbol": "VRSC"
    },  # VRSC
    "i9nLSK4S1U5sVMq4eJUHR1gbFALz56J9Lj": {
        "address": "0x0655977FEb2f289A4aB78af67BAB0d17aAb84367",
        "eth_symbol": "CRVUSD",
        "vrsc_symbol": "scrvUSD.vETH"
    },  # scrvUSD.vETH
    "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU": {
        "address": "0x18084fbA666a33d37592fA2633fD49a74DD93a88",
        "eth_symbol": "TBTC",
        "vrsc_symbol": "tBTC.vETH"
    },  # tBTC.vETH
    "iExBJfZYK7KREDpuhj6PzZBzqMAKaFg7d2": {
        "address": "0x45766AE12411450e20bd1c8cca1e63DffD834e19",
        "eth_symbol": "VARR",
        "vrsc_symbol": "vARRR"
    },  # vARRR (native)
    "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd": {
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "eth_symbol": "USDC",
        "vrsc_symbol": "vUSDC.vETH"
    },  # vUSDC.vETH
    "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY": {
        "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "eth_symbol": "USDT",
        "vrsc_symbol": "vUSDT.vETH"
    },  # vUSDT.vETH
    "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X": {
        "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "eth_symbol": "WETH",
        "vrsc_symbol": "vETH"
    },  # vETH --> WETH
    "iJ3WZocnjG9ufv7GKUA4LijQno5gTMb7tP": {
        "address": "0x714cFa2DA83b53b8fe2c1c9F99ca723A4c61AD48",
        "eth_symbol": "CHIPS",
        "vrsc_symbol": "CHIPS"
    },  # CHIPS (native)
    "i6SapneNdvpkrLPgqPhDVim7Ljek3h2UQZ": {
        "address": "0x504DAa3346f4AE4E624932FD654339Ad971FB242",
        "eth_symbol": "SUPERNET",
        "vrsc_symbol": "SUPERNET"
    },  # SUPERNET (native)
    "iHog9UCTrn95qpUBFCZ7kKz7qWdMA8MQ6N": {
        "address": "0x0609Aede2f67C136bcb0e413E298F6cA8e283c37",
        "eth_symbol": "VDEX",
        "vrsc_symbol": "vDEX"
    },  # vDEX (native)
}   

# Required helper functions for currency name normalization
def normalize_currency_name(name):
    """Normalize currency name - DISABLED for now to use actual currency names
    
    Args:
        name (str): Currency name to normalize
        
    Returns:
        str: Currency name unchanged (normalization disabled)
    """
    # Normalization disabled - return actual currency names
    return name

def get_ticker_by_id(currency_id):
    """Get ticker symbol from currency ID using currency_contract_mapping
    
    Args:
        currency_id (str): Currency ID to look up
        
    Returns:
        str: Ticker symbol if found, otherwise the original ID
    """
    # First try to look up in our currency_contract_mapping
    contract_info = currency_contract_mapping.get(currency_id)
    if contract_info and isinstance(contract_info, dict):
        # Use VRSC symbol as the default ticker
        return contract_info.get('vrsc_symbol')
    
    # If not found, extract from the ID name if possible
    if '.' in currency_id:
        return currency_id  # Use full currency ID, no short names
    
    # Default: return original ID
    return currency_id

def get_mapped_eth_address(currency_id):
    """Get Ethereum contract address for a currency ID from mapping
    
    Args:
        currency_id (str): Currency ID to look up
        
    Returns:
        str: Ethereum contract address or None if not found
    """
    contract_info = currency_contract_mapping.get(currency_id)
    if contract_info and isinstance(contract_info, dict):
        return contract_info.get('address')
    return None

def get_mapped_eth_symbol(currency_id):
    """Get Ethereum symbol for a currency ID from mapping
    
    Args:
        currency_id (str): Currency ID to look up
        
    Returns:
        str: ETH symbol or None if not found
    """
    contract_info = currency_contract_mapping.get(currency_id)
    if contract_info and isinstance(contract_info, dict):
        return contract_info.get('eth_symbol')
    return None

def get_mapped_vrsc_symbol(currency_id):
    """Get VRSC symbol for a currency ID from mapping
    
    Args:
        currency_id (str): Currency ID to look up
        
    Returns:
        str: VRSC symbol or None if not found
    """
    contract_info = currency_contract_mapping.get(currency_id)
    if contract_info and isinstance(contract_info, dict):
        return contract_info.get('vrsc_symbol')
    return None

def get_symbol_for_currency(currency_id):
    """Get appropriate symbol for a currency ID (ETH for exported, VRSC for native)
    
    Args:
        currency_id (str): Currency ID to look up
        
    Returns:
        str: ETH symbol if currency is exported to Ethereum, VRSC symbol otherwise, or None if not found
    """
    contract_info = currency_contract_mapping.get(currency_id)
    if contract_info and isinstance(contract_info, dict):
        # If currency has an Ethereum contract address, use ETH symbol
        if contract_info.get('address'):
            return contract_info.get('eth_symbol')
        # Otherwise use VRSC symbol
        else:
            return contract_info.get('vrsc_symbol')
    return None

def is_currency_exported_to_ethereum(currency_id):
    """Check if currency is exported to Ethereum (has contract address)
    
    Args:
        currency_id (str): Currency ID to check
        
    Returns:
        bool: True if currency has Ethereum contract address
    """
    return currency_id in currency_contract_mapping

def is_converter_currency(currency_id):
    """Check if a currency ID is a converter currency (multi-currency basket)
    
    Args:
        currency_id (str): Currency ID to check
        
    Returns:
        bool: True if currency is a converter, False otherwise
    """
    return currency_id in converter_ids

def get_currency_info_by_id(currency_id):
    """Get complete currency information from currency ID
    
    Args:
        currency_id (str): Currency ID to look up
        
    Returns:
        dict: Currency info with ticker and contract address if available
    """
    # Get ticker from currency_names
    ticker = get_ticker_by_id(currency_id)
    
    # Get contract address if available
    contract_address = get_mapped_eth_address(currency_id)
    
    return {
        "currencyid": currency_id,
        "ticker": ticker,
        "mappedethaddress": contract_address
    }
