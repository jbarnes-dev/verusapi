#!/usr/bin/env python3
"""
I-Address CoinMarketCap Formatter
Creates CoinMarketCap-style endpoint using i-addresses as keys instead of ERC20 contract addresses
This is a separate implementation for testing purposes - does not modify existing CoinMarketCap endpoint
"""

from collections import defaultdict
from typing import List, Dict, Any
import logging

def aggregate_pairs_for_iaddress_cmc(pairs_data: List[Dict]) -> Dict:
    """
    Aggregate pairs for i-address CoinMarketCap format using i-addresses as keys
    Similar to CoinMarketCap aggregation but uses currency IDs instead of contract addresses
    """
    try:
        from dict import is_converter_currency
        
        pair_aggregation = {}
        
        excluded_count = 0
        processed_count = 0
        
        for pair_data in pairs_data:
            # Debug: Check data type
            if not isinstance(pair_data, dict):
                logging.error(f"Invalid pair_data type: {type(pair_data)}, value: {pair_data}")
                continue
                
            base_currency_id = pair_data.get('base_currency_id', '')
            target_currency_id = pair_data.get('target_currency_id', '')
            
            # Skip converter currencies
            if is_converter_currency(base_currency_id) or is_converter_currency(target_currency_id):
                excluded_count += 1
                continue
            
            base_currency = pair_data.get('base_currency', '')
            target_currency = pair_data.get('target_currency', '')
            
            # Create composite key using i-addresses
            pair_key = f"{base_currency_id}_{target_currency_id}"
            
            base_volume = float(pair_data.get('base_volume', 0))
            target_volume = float(pair_data.get('target_volume', 0))
            last_price = float(pair_data.get('last', 0))  # Use 'last' field like Enhanced CMC
            
            # Only include pairs with volume
            if base_volume <= 0:
                continue
            
            processed_count += 1
            
            if pair_key in pair_aggregation:
                # Aggregate with existing data (same logic as Enhanced CMC)
                existing = pair_aggregation[pair_key]
                
                # Sum volumes
                existing_base_vol = float(existing['base_volume'])
                existing_quote_vol = float(existing['quote_volume'])
                new_base_vol = base_volume
                new_quote_vol = target_volume
                
                total_base_vol = existing_base_vol + new_base_vol
                total_quote_vol = existing_quote_vol + new_quote_vol
                
                # Volume-weighted average price (using quote volume as weight - same as Enhanced CMC)
                existing_price = float(existing['last_price'])
                new_price = last_price
                
                if existing_quote_vol + new_quote_vol > 0:
                    weighted_price = (existing_price * existing_quote_vol + new_price * new_quote_vol) / (existing_quote_vol + new_quote_vol)
                else:
                    weighted_price = new_price  # Fallback to new price
                
                # Update aggregated data
                pair_aggregation[pair_key].update({
                    'last_price': f"{weighted_price:.8f}",
                    'base_volume': f"{total_base_vol:.8f}",
                    'quote_volume': f"{total_quote_vol:.8f}"
                })
                
                logging.debug(f"📊 Aggregated {pair_key}: quote volumes {existing_quote_vol:.2f}+{new_quote_vol:.2f}={total_quote_vol:.2f}")
            else:
                # First occurrence of this pair
                ticker = {
                    'base_id': base_currency_id,
                    'base_name': base_currency,  # Verus native symbol
                    'base_symbol': base_currency,  # Verus native symbol
                    'quote_id': target_currency_id,
                    'quote_name': target_currency,  # Verus native symbol
                    'quote_symbol': target_currency,  # Verus native symbol
                    'last_price': f"{last_price:.8f}",
                    'base_volume': f"{base_volume:.8f}",
                    'quote_volume': f"{target_volume:.8f}"
                }
                pair_aggregation[pair_key] = ticker
        
        logging.info(f"I-Address CMC aggregation: {excluded_count} excluded, {processed_count} processed, {len(pair_aggregation)} final pairs")
        return pair_aggregation
        
    except Exception as e:
        logging.error(f"Error in i-address CMC aggregation: {str(e)}")
        return {}

def format_iaddress_coinmarketcap_tickers(pairs_data: List[Dict]) -> Dict:
    """
    Format tickers for i-address CoinMarketCap endpoint
    Uses i-addresses as identifiers instead of ERC20 contract addresses
    """
    try:
        if not pairs_data:
            logging.warning("No pairs data provided for i-address CMC formatting")
            return {}
        
        logging.info(f"Formatting {len(pairs_data)} pairs for i-address CoinMarketCap endpoint")
        
        # Aggregate pairs using i-addresses
        aggregated_tickers = aggregate_pairs_for_iaddress_cmc(pairs_data)
        
        if not aggregated_tickers:
            logging.warning("No aggregated tickers generated for i-address CMC endpoint")
            return {}
        
        logging.info(f"Successfully formatted {len(aggregated_tickers)} i-address CMC tickers")
        return aggregated_tickers
        
    except Exception as e:
        logging.error(f"Error formatting i-address CMC tickers: {str(e)}")
        return {}

def format_iaddress_coinmarketcap_tickers_cached(pairs_data: List[Dict]) -> Dict:
    """
    Cached version of i-address CoinMarketCap formatter
    """
    return format_iaddress_coinmarketcap_tickers(pairs_data)
