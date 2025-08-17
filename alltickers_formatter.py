"""
AllTickers Formatter - VerusStatisticsAPI Compatible
==================================================

Creates an endpoint that outputs data in the same format as:
https://marketapi.verus.services/market/allTickers

But uses our existing reliable data source (same as CoinMarketCap) with:
- ERC20 symbols from currency_contract_mapping
- Same-pair aggregation (NO inverse pair aggregation)
- Proper exclusion of converter currencies and excluded chains
- Volume-weighted price aggregation
- 8-decimal string formatting to prevent scientific notation
"""

import logging
from typing import Dict, List
from collections import defaultdict
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_erc20_symbol(currency_id: str, fallback_symbol: str) -> str:
    """
    Get ERC20 symbol for a currency, with fallback to VRSC symbol
    
    Args:
        currency_id: The currency ID to look up
        fallback_symbol: Fallback symbol if no ERC20 mapping exists
        
    Returns:
        ERC20 symbol or fallback symbol
    """
    try:
        from dict import currency_contract_mapping
        
        if currency_id in currency_contract_mapping:
            return currency_contract_mapping[currency_id]["eth_symbol"]
        
        # For currencies without ERC20 mapping, use the fallback
        return fallback_symbol
        
    except Exception as e:
        logger.warning(f"Error getting ERC20 symbol for {currency_id}: {e}")
        return fallback_symbol

def should_exclude_pair(base_currency_id: str, target_currency_id: str, base_symbol: str, target_symbol: str) -> bool:
    """
    Check if a pair should be excluded based on converter IDs and excluded chains
    
    Args:
        base_currency_id: Base currency ID
        target_currency_id: Target currency ID  
        base_symbol: Base currency symbol
        target_symbol: Target currency symbol
        
    Returns:
        True if pair should be excluded, False otherwise
    """
    try:
        from dict import converter_ids, excluded_chains, is_converter_currency
        
        # Exclude if either currency is a converter currency
        if is_converter_currency(base_currency_id) or is_converter_currency(target_currency_id):
            return True
            
        # Exclude if either symbol is in excluded chains
        if base_symbol in excluded_chains or target_symbol in excluded_chains:
            return True
            
        return False
        
    except Exception as e:
        logger.warning(f"Error checking exclusion for {base_symbol}-{target_symbol}: {e}")
        return False

def aggregate_pairs_for_alltickers(pairs_data: List[Dict]) -> Dict:
    """
    Aggregate pairs for allTickers format using same-pair aggregation (NO inverse aggregation)
    
    Args:
        pairs_data: List of pair data dictionaries
        
    Returns:
        Dictionary of aggregated ticker data
    """
    try:
        pair_aggregation = defaultdict(lambda: {
            'base_volume': 0.0,
            'target_volume': 0.0,
            'price_sum': 0.0,
            'price_weight': 0.0,
            'high_price': 0.0,
            'low_price': float('inf'),
            'base_symbol': '',
            'target_symbol': '',
            'count': 0,
            'valid_prices': False
        })
        
        excluded_count = 0
        processed_count = 0
        
        for pair_data in pairs_data:
            base_currency_id = pair_data.get('base_currency_id', '')
            target_currency_id = pair_data.get('target_currency_id', '')
            base_currency = pair_data.get('base_currency', '')
            target_currency = pair_data.get('target_currency', '')
            
            # Check if pair should be excluded
            if should_exclude_pair(base_currency_id, target_currency_id, base_currency, target_currency):
                excluded_count += 1
                continue
            
            # Get ERC20 symbols
            base_erc_symbol = get_erc20_symbol(base_currency_id, base_currency)
            target_erc_symbol = get_erc20_symbol(target_currency_id, target_currency)
            
            # Create pair key (same-pair aggregation, no inverse)
            pair_key = f"{base_erc_symbol}_{target_erc_symbol}"
            
            base_volume = float(pair_data.get('base_volume', 0))
            target_volume = float(pair_data.get('target_volume', 0))
            last_price = float(pair_data.get('last_price', 0))
            high_price = float(pair_data.get('high', 0))
            low_price = float(pair_data.get('low', 0))
            
            if base_volume <= 0:
                continue
            
            processed_count += 1
            agg = pair_aggregation[pair_key]
            
            # Set symbols on first encounter
            if not agg['base_symbol']:
                agg['base_symbol'] = base_erc_symbol
                agg['target_symbol'] = target_erc_symbol
            
            # Aggregate volumes
            agg['base_volume'] += base_volume
            agg['target_volume'] += target_volume
            
            # Handle price aggregation with fallback
            effective_price = last_price
            if last_price <= 0 and high_price > 0 and low_price > 0:
                effective_price = (high_price + low_price) / 2
            
            if effective_price > 0:
                weight = target_volume  # Use quote volume as weight (same as Enhanced CMC)
                agg['price_sum'] += effective_price * weight
                agg['price_weight'] += weight
                agg['valid_prices'] = True
            
            # Track high/low prices
            if high_price > 0:
                agg['high_price'] = max(agg['high_price'], high_price)
            if low_price > 0:
                if agg['low_price'] == float('inf'):
                    agg['low_price'] = low_price
                else:
                    agg['low_price'] = min(agg['low_price'], low_price)
            
            agg['count'] += 1
        
        # Generate final tickers
        final_tickers = []
        
        for pair_key, agg in pair_aggregation.items():
            if agg['base_volume'] > 0:
                # Calculate weighted average price
                if agg['price_weight'] > 0 and agg['valid_prices']:
                    weighted_avg_price = agg['price_sum'] / agg['price_weight']
                else:
                    weighted_avg_price = 0.0
                
                # Handle infinite low price
                if agg['low_price'] == float('inf'):
                    agg['low_price'] = weighted_avg_price
                
                # Create ticker in allTickers format
                ticker = {
                    'symbol': f"{agg['base_symbol']}-{agg['target_symbol']}",
                    'symbolName': f"{agg['base_symbol']}-{agg['target_symbol']}",
                    'volume': f"{agg['base_volume']:.8f}",
                    'last': f"{weighted_avg_price:.8f}",
                    'high': f"{agg['high_price']:.8f}",
                    'low': f"{agg['low_price']:.8f}",
                    'open': f"{agg['high_price']:.8f}"  # Using high as open (same as original)
                }
                
                final_tickers.append(ticker)
        
        # Sort by volume (descending)
        final_tickers.sort(key=lambda x: float(x['volume']), reverse=True)
        
        logger.info(f"✅ AllTickers: processed {processed_count} pairs, generated {len(final_tickers)} tickers (excluded {excluded_count} pairs)")
        return final_tickers
        
    except Exception as e:
        logger.error(f"Error in aggregate_pairs_for_alltickers: {e}")
        return []

def generate_alltickers_response() -> List[Dict]:
    """
    Generate allTickers response using our reliable data source
    
    Returns:
        List of ticker dictionaries in allTickers format
    """
    try:
        from data_integration import extract_all_pairs_data
        
        logger.info("🚀 Generating allTickers response with ERC20 symbols")
        
        # Get pairs data (same source as CoinMarketCap)
        pairs_data = extract_all_pairs_data()
        
        if not pairs_data or 'pairs' not in pairs_data:
            logger.error("No pairs data available for allTickers")
            return []
        
        pairs_list = pairs_data['pairs']
        if not isinstance(pairs_list, list) or len(pairs_list) == 0:
            logger.error("Invalid pairs data for allTickers")
            return []
        
        # Aggregate pairs using allTickers logic
        tickers = aggregate_pairs_for_alltickers(pairs_list)
        
        logger.info(f"✅ Generated allTickers response with {len(tickers)} tickers")
        return tickers
        
    except Exception as e:
        import traceback
        logger.error(f"Error generating allTickers response: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []

def generate_alltickers_response_cached() -> List[Dict]:
    """
    Generate allTickers response using cached data
    
    Returns:
        List of ticker dictionaries in allTickers format
    """
    try:
        from ticker_formatting_cached import get_cached_pairs_data
        
        logger.info("🚀 Generating allTickers cached response with ERC20 symbols")
        
        # Get cached pairs data
        cached_data = get_cached_pairs_data()
        
        if 'error' in cached_data:
            logger.error(f"Error getting cached data: {cached_data['error']}")
            return []
        
        pairs_list = cached_data.get('pairs', [])
        if not isinstance(pairs_list, list) or len(pairs_list) == 0:
            logger.error("No cached pairs data available for allTickers")
            return []
        
        # Aggregate pairs using allTickers logic
        tickers = aggregate_pairs_for_alltickers(pairs_list)
        
        logger.info(f"✅ Generated allTickers cached response with {len(tickers)} tickers")
        return tickers
        
    except Exception as e:
        import traceback
        logger.error(f"Error generating allTickers cached response: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []
