#!/usr/bin/env python3
"""
Cached Ticker Formatting Module for Verus Ticker API
Uses unified caching to improve performance and reduce RPC calls
"""

from datetime import datetime
from typing import Dict, List
import logging

# Import the original formatting functions
from ticker_formatting import (
    format_coingecko_ticker,
    format_coingecko2_ticker,
    format_cmc_dex_ticker,
    format_cmc_enhanced_ticker,
    format_verus_statistics_ticker,
    format_verus_statistics_ticker_enhanced,
    get_currency_full_name,
    get_converter_pool_id,
    get_pair_liquidity
)

# Import cache manager
from cache_manager import get_cached_pairs_data, get_cache_status

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_formatted_tickers_cached(format_type: str = "coingecko") -> Dict:
    """
    Get formatted ticker data using unified caching
    
    Args:
        format_type: "coingecko", "verus_statistics", "verus_statistics_enhanced", or "cmc"
    
    Returns:
        Dict containing formatted ticker data with cache information
    """
    try:
        # Import data integration functions
        from data_integration import load_converter_data
        
        # Get raw ticker data from cache (or fresh if cache expired)
        raw_data = get_cached_pairs_data()
        
        if 'error' in raw_data:
            return {
                'error': raw_data['error'],
                'timestamp': datetime.utcnow().isoformat(),
                'cache_info': get_cache_status()
            }
        
        pairs_data = raw_data.get('pairs', [])
        
        if format_type == "coingecko":
            formatted_tickers = format_coingecko_response_cached(pairs_data)
            return {
                'success': True,
                'format': 'coingecko_cached',
                'timestamp': datetime.utcnow().isoformat(),
                'total_pairs': len(formatted_tickers),
                'tickers': formatted_tickers,
                'metadata': {
                    'block_range': raw_data.get('block_range', {}),
                    'total_converters': raw_data.get('total_converters', 0)
                },
                'cache_info': get_cache_status()
            }
            
        elif format_type == "verus_statistics":
            formatted_response = format_verus_statistics_response_cached(pairs_data)
            # Add cache info to the response
            formatted_response['cache_info'] = get_cache_status()
            return formatted_response
            
        elif format_type == "verus_statistics_enhanced":
            formatted_response = format_verus_statistics_response_enhanced_cached(pairs_data)
            # Add cache info to the response
            formatted_response['cache_info'] = get_cache_status()
            return formatted_response
            
        elif format_type == "cmc":
            formatted_tickers = generate_coinmarketcap_tickers_cached(pairs_data)
            return {
                'tickers': formatted_tickers,
                'cache_info': get_cache_status()
            }
            
        else:
            return {
                'error': f'Unknown format type: {format_type}',
                'available_formats': ['coingecko', 'verus_statistics', 'verus_statistics_enhanced', 'cmc'],
                'cache_info': get_cache_status()
            }
            
    except Exception as e:
        logger.error(f"Error in get_formatted_tickers_cached: {str(e)}")
        return {
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
            'cache_info': get_cache_status()
        }

def format_coingecko_response_cached(pairs_data: List[Dict]) -> List[Dict]:
    """
    Format all pairs data into CoinGecko API response format (cached version)
    Excludes pairs containing converter currencies (multi-currency baskets)
    
    Args:
        pairs_data: List of raw pair data
    
    Returns:
        List of CoinGecko formatted tickers (excluding converter currency pairs)
    """
    try:
        from dict import is_converter_currency
        
        tickers = []
        excluded_count = 0
        
        logger.info(f"🚀 Processing {len(pairs_data)} pairs for CoinGecko format (cached)")
        
        for i, pair in enumerate(pairs_data):
            logger.debug(f"Processing pair {i}: type={type(pair)}")
            if isinstance(pair, dict):
                # Get currency IDs for filtering
                base_currency_id = pair.get('base_currency_id', '')
                target_currency_id = pair.get('target_currency_id', '')
                
                # Skip pairs that include converter currencies
                if is_converter_currency(base_currency_id) or is_converter_currency(target_currency_id):
                    excluded_count += 1
                    logger.debug(f"🚫 Excluding converter pair: {pair.get('base_currency', '')}-{pair.get('target_currency', '')}")
                    continue
                
                ticker = format_coingecko2_ticker(pair)
                if ticker:  # Only add valid tickers
                    tickers.append(ticker)
            else:
                logger.error(f"Pair {i} is not a dict: {type(pair)} - {pair}")
        
        logger.info(f"✅ Formatted {len(tickers)} CoinGecko tickers from {len(pairs_data)} pairs (cached, excluded {excluded_count} converter pairs)")
        return tickers
        
    except Exception as e:
        logger.error(f"Error formatting CoinGecko response (cached): {e}")
        return []

def format_verus_statistics_response_cached(pairs_data: List[Dict]) -> Dict:
    """
    Format all pairs data into VerusStatistics API response format (cached version)
    
    Args:
        pairs_data: List of raw pair data
    
    Returns:
        Dict in VerusStatistics API format
    """
    try:
        tickers = []
        
        for pair in pairs_data:
            ticker = format_verus_statistics_ticker(pair)
            if ticker:  # Only add valid tickers
                tickers.append(ticker)
        
        # Create VerusStatistics API response structure
        response = {
            "code": "200000",
            "data": {
                "time": int(datetime.utcnow().timestamp() * 1000),  # Milliseconds
                "ticker": tickers
            }
        }
        
        logger.info(f"✅ Formatted {len(tickers)} VerusStatistics tickers from {len(pairs_data)} pairs (cached)")
        return response
        
    except Exception as e:
        logger.error(f"Error formatting VerusStatistics response (cached): {e}")
        return {
            "code": "500000",
            "data": {
                "time": int(datetime.utcnow().timestamp() * 1000),
                "ticker": []
            }
        }

def format_verus_statistics_response_enhanced_cached(pairs_data: List[Dict]) -> Dict:
    """
    Format all pairs data into enhanced VerusStatistics API response format (cached version)
    
    Args:
        pairs_data: List of raw pair data
    
    Returns:
        Dict in enhanced VerusStatistics API format
    """
    try:
        tickers = []
        
        for pair in pairs_data:
            ticker = format_verus_statistics_ticker_enhanced(pair)
            if ticker:  # Only add valid tickers
                tickers.append(ticker)
        
        # Create VerusStatistics API response structure
        response = {
            "code": "200000",
            "data": {
                "time": int(datetime.utcnow().timestamp() * 1000),  # Milliseconds
                "ticker": tickers
            }
        }
        
        logger.info(f"✅ Formatted {len(tickers)} enhanced VerusStatistics tickers from {len(pairs_data)} pairs (cached)")
        return response
        
    except Exception as e:
        logger.error(f"Error formatting enhanced VerusStatistics response (cached): {e}")
        return {
            "code": "500000",
            "data": {
                "time": int(datetime.utcnow().timestamp() * 1000),
                "ticker": []
            }
        }

def generate_coinmarketcap_tickers_cached(pairs_data: List[Dict]) -> Dict:
    """
    Generate CoinMarketCap (CMC) DEX format tickers from pairs data (cached version)
    Excludes pairs containing converter currencies (multi-currency baskets)
    
    Args:
        pairs_data: List of pair data from data integration
    
    Returns:
        Dictionary with sequential keys and ticker data (CMC DEX object format)
    """
    try:
        from dict import is_converter_currency
        
        cmc_tickers = {}
        key_counter = 1
        excluded_count = 0
        
        for pair_data in pairs_data:
            # Get currency IDs for filtering
            base_currency_id = pair_data.get('base_currency_id', '')
            target_currency_id = pair_data.get('target_currency_id', '')
            
            # Skip pairs that include converter currencies
            if is_converter_currency(base_currency_id) or is_converter_currency(target_currency_id):
                excluded_count += 1
                logger.debug(f"🚫 Excluding converter pair: {pair_data.get('base_currency', '')}-{pair_data.get('target_currency', '')}")
                continue
            
            composite_key, ticker_data = format_cmc_dex_ticker(pair_data)
            if composite_key and ticker_data:
                # Use composite keys as per original format
                cmc_tickers[composite_key] = ticker_data
        
        logger.info(f"✅ Generated {len(cmc_tickers)} CMC DEX tickers (cached, excluded {excluded_count} converter pairs)")
        return cmc_tickers
        
    except Exception as e:
        logger.error(f"Error generating CMC DEX tickers (cached): {e}")
        return {}

def generate_coinmarketcap_enhanced_tickers_cached(pairs_data: List[Dict]) -> Dict:
    """
    Generate Enhanced CoinMarketCap (CMC) DEX format tickers with Ethereum contract details (cached version)
    Uses contract addresses and symbols (e.g., WETH instead of ETH) when available
    Excludes pairs containing converter currencies (multi-currency baskets)
    Aggregates data from multiple converters with the same trading pair per CMC DEX spec
    
    Args:
        pairs_data: List of pair data from data integration
    
    Returns:
        Dictionary with composite keys and aggregated ticker data (CMC DEX object format)
        Uses proper composite keys per CMC DEX specification (excluding converter pairs)
    """
    try:
        from dict import is_converter_currency
        
        # Temporary storage for aggregation
        pair_aggregation = {}
        excluded_count = 0
        
        for pair_data in pairs_data:
            # Get currency IDs for filtering
            base_currency_id = pair_data.get('base_currency_id', '')
            target_currency_id = pair_data.get('target_currency_id', '')
            
            # Skip pairs that include converter currencies
            if is_converter_currency(base_currency_id) or is_converter_currency(target_currency_id):
                excluded_count += 1
                logger.debug(f"🚫 Excluding converter pair: {pair_data.get('base_currency', '')}-{pair_data.get('target_currency', '')}")
                continue
            
            composite_key, ticker_data = format_cmc_enhanced_ticker(pair_data)
            if composite_key and ticker_data:
                if composite_key in pair_aggregation:
                    # Aggregate with existing data
                    existing = pair_aggregation[composite_key]
                    
                    # Sum volumes
                    existing_base_vol = float(existing['base_volume'])
                    existing_quote_vol = float(existing['quote_volume'])
                    new_base_vol = float(ticker_data['base_volume'])
                    new_quote_vol = float(ticker_data['quote_volume'])
                    
                    total_base_vol = existing_base_vol + new_base_vol
                    total_quote_vol = existing_quote_vol + new_quote_vol
                    
                    # Volume-weighted average price (using quote volume as weight)
                    existing_price = float(existing['last_price'])
                    new_price = float(ticker_data['last_price'])
                    
                    if existing_quote_vol + new_quote_vol > 0:
                        weighted_price = (existing_price * existing_quote_vol + new_price * new_quote_vol) / (existing_quote_vol + new_quote_vol)
                    else:
                        weighted_price = new_price  # Fallback to new price
                    
                    # Update aggregated data
                    pair_aggregation[composite_key].update({
                        'last_price': f"{weighted_price:.8f}",
                        'base_volume': f"{total_base_vol:.8f}",
                        'quote_volume': f"{total_quote_vol:.8f}"
                    })
                    
                    logger.debug(f"📊 Aggregated {composite_key}: volumes {existing_base_vol:.2f}+{new_base_vol:.2f}={total_base_vol:.2f}")
                else:
                    # First occurrence of this pair
                    pair_aggregation[composite_key] = ticker_data
        
        logger.info(f"✅ Generated {len(pair_aggregation)} enhanced CMC DEX tickers with aggregation (cached, excluded {excluded_count} converter pairs)")
        return pair_aggregation
        
    except Exception as e:
        logger.error(f"Error generating enhanced CMC DEX tickers (cached): {e}")
        return {}

# Cache management functions for API endpoints
def get_cache_info() -> Dict:
    """
    Get cache information for monitoring
    
    Returns:
        Dict: Cache status and information
    """
    return get_cache_status()

# CLEAN STANDARD-COMPLIANT CACHED FUNCTIONS (NO METADATA)
# These functions return pure standard formats for production use

def get_clean_coingecko_tickers_cached() -> List[Dict]:
    """
    Get CoinGecko tickers in pure standard format (NO metadata)
    
    Returns:
        List: Pure CoinGecko ticker array (standard compliant)
    """
    try:
        # Get raw ticker data from cache
        raw_data = get_cached_pairs_data()
        
        if 'error' in raw_data:
            logger.error(f"Error getting cached data: {raw_data['error']}")
            return []
        
        pairs_data = raw_data.get('pairs', [])
        return format_coingecko_response_cached(pairs_data)
        
    except Exception as e:
        logger.error(f"Error in get_clean_coingecko_tickers_cached: {str(e)}")
        return []

def get_clean_coinmarketcap_tickers_cached() -> Dict:
    """
    Get CoinMarketCap tickers in pure standard format (NO metadata)
    
    Returns:
        Dict: Pure CoinMarketCap object with sequential keys (standard compliant)
    """
    try:
        # Get raw ticker data from cache
        raw_data = get_cached_pairs_data()
        
        if 'error' in raw_data:
            logger.error(f"Error getting cached data: {raw_data['error']}")
            return {}
        
        pairs_data = raw_data.get('pairs', [])
        return generate_coinmarketcap_tickers_cached(pairs_data)
        
    except Exception as e:
        logger.error(f"Error in get_clean_coinmarketcap_tickers_cached: {str(e)}")
        return {}

def get_clean_coinmarketcap_enhanced_tickers_cached() -> Dict:
    """
    Get Enhanced CoinMarketCap tickers in pure standard format (NO metadata)
    
    Returns:
        Dict: Pure Enhanced CoinMarketCap object with sequential keys (standard compliant)
    """
    try:
        # Get raw ticker data from cache
        raw_data = get_cached_pairs_data()
        
        if 'error' in raw_data:
            logger.error(f"Error getting cached data: {raw_data['error']}")
            return {}
        
        pairs_data = raw_data.get('pairs', [])
        return generate_coinmarketcap_enhanced_tickers_cached(pairs_data)
        
    except Exception as e:
        logger.error(f"Error in get_clean_coinmarketcap_enhanced_tickers_cached: {str(e)}")
        return {}

# Coinpaprika cached function removed for clean restart

def clear_cache() -> Dict:
    """
    Clear the cache manually
    
    Returns:
        Dict: Status message
    """
    from cache_manager import invalidate_cache
    
    try:
        invalidate_cache()
        return {
            'success': True,
            'message': 'Cache cleared successfully',
            'timestamp': datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }
