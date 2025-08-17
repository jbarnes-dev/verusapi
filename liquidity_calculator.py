#!/usr/bin/env python3
"""
Liquidity Calculator Module
Implements pair liquidity calculation using proven working code from Deploy
Formula: Pair Liquidity = Total Converter Liquidity × (Weight of Currency A + Weight of Currency B)
"""

import json
import logging
from typing import Dict, Optional
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verus_rpc import make_rpc_call
from dict import get_ticker_by_id
from block_height import get_session_block_height

logger = logging.getLogger(__name__)

def get_vrsc_usd_price_cached():
    """
    Get VRSC to USD price using DAI estimation
    Uses session-based caching for consistency
    """
    try:
        # Use estimateconversion to get VRSC to DAI.vETH rate via Bridge.vETH
        conversion_params = {'currency': 'VRSC', 'convertto': 'DAI.vETH', 'amount': 1, 'via': 'Bridge.vETH'}
        result = make_rpc_call('VRSC', 'estimateconversion', [conversion_params])
        
        if result and 'estimatedcurrencyout' in result:
            vrsc_dai_rate = float(result['estimatedcurrencyout'])
            # Assume DAI.vETH ≈ 1 USD for simplicity
            return vrsc_dai_rate
        
        return 0.0
    except Exception as e:
        logger.error(f"Error getting VRSC→USD price: {e}")
        return 0.0

def get_converter_liquidity(converter_name: str, converters_data: Dict) -> float:
    """
    Calculate total liquidity for a converter in USD
    Based on proven working code from Deploy/batch_api_v2.py
    
    Args:
        converter_name: Name of the converter
        converters_data: Converter discovery data
        
    Returns:
        Total liquidity in USD
    """
    try:
        # Find the converter in the data
        converter_info = None
        for conv in converters_data:
            if conv.get('name') == converter_name:
                converter_info = conv
                break
        
        if not converter_info:
            logger.error(f"Converter {converter_name} not found in data")
            return 0.0
        
        converter_id = converter_info.get('currency_id')
        supply = converter_info.get('supply', 0)
        
        if not converter_id or supply <= 0:
            logger.error(f"Invalid converter ID or supply for {converter_name}")
            return 0.0
        
        # Step 1: Get converter to VRSC conversion ratio
        vrsc_ratio = 0
        try:
            conversion_params = {'currency': converter_id, 'convertto': 'VRSC', 'amount': 1}
            conversion_result = make_rpc_call('VRSC', 'estimateconversion', [conversion_params])
            
            if conversion_result and 'estimatedcurrencyout' in conversion_result:
                vrsc_ratio = float(conversion_result['estimatedcurrencyout'])
        except Exception as e:
            logger.error(f"Error getting {converter_name} to VRSC conversion: {e}")
        
        if vrsc_ratio <= 0:
            logger.error(f"Could not get valid VRSC ratio for {converter_name}")
            return 0.0
        
        # Step 2: Get VRSC to USD price
        vrsc_usd_price = get_vrsc_usd_price_cached()
        
        if vrsc_usd_price <= 0:
            logger.error(f"Could not get valid VRSC→USD price")
            return 0.0
        
        # Step 3: Calculate total liquidity = supply × VRSC_ratio × VRSC_USD_price
        total_liquidity = supply * vrsc_ratio * vrsc_usd_price
        
        logger.info(f"Liquidity calculation for {converter_name}:")
        logger.info(f"  Supply: {supply}")
        logger.info(f"  VRSC ratio: {vrsc_ratio}")
        logger.info(f"  VRSC USD price: {vrsc_usd_price}")
        logger.info(f"  Total liquidity: ${total_liquidity:.2f}")
        
        return total_liquidity
        
    except Exception as e:
        logger.error(f"Error calculating converter liquidity for {converter_name}: {e}")
        return 0.0

def get_pair_liquidity(converter_name: str, base_currency: str, target_currency: str, converters_data: Dict) -> float:
    """
    Calculate the liquidity for a specific trading pair in a converter
    Formula: (weight1 + weight2) / total_weight * total_liquidity
    Based on proven working code from Deploy/batch_api_v2.py
    
    Args:
        converter_name: Name of the converter
        base_currency: Base currency of the pair
        target_currency: Target currency of the pair
        converters_data: Converter discovery data
        
    Returns:
        Pair liquidity in USD
    """
    try:
        # Get total converter liquidity first
        total_liquidity = get_converter_liquidity(converter_name, converters_data)
        
        if total_liquidity <= 0:
            return 0.0
        
        # Find the converter in the data
        converter_info = None
        for conv in converters_data:
            if conv.get('name') == converter_name:
                converter_info = conv
                break
        
        if not converter_info:
            logger.error(f"Converter {converter_name} not found in data")
            return 0.0
        
        # Get weights for the currencies
        base_weight = 0
        target_weight = 0
        total_weight = 0
        
        reserve_currencies = converter_info.get('reserve_currencies', [])
        for rc in reserve_currencies:
            weight = float(rc.get('weight', 0))
            total_weight += weight
            
            currency_ticker = rc.get('ticker', '')
            
            if currency_ticker == base_currency:
                base_weight = weight
            if currency_ticker == target_currency:
                target_weight = weight
        
        # Check if this is a special case (converter currency is one of the pair currencies)
        base_is_converter = (base_currency == converter_name)
        target_is_converter = (target_currency == converter_name)
        is_special_case = base_is_converter or target_is_converter
        
        if is_special_case:
            # Special case: one currency is the converter itself
            # Find the weight of the non-converter currency
            non_converter_weight = target_weight if base_is_converter else base_weight
            
            if non_converter_weight > 0 and total_weight > 0:
                # Formula: (weight * total_liquidity) * 2
                weight_fraction = non_converter_weight / total_weight
                pair_liquidity = (weight_fraction * total_liquidity) * 2
                return pair_liquidity
            else:
                return 0.0
        else:
            # Regular case: both currencies are reserve currencies
            if base_weight > 0 and target_weight > 0 and total_weight > 0:
                # Formula: (weight1 + weight2) / total_weight * total_liquidity
                combined_weight_fraction = (base_weight + target_weight) / total_weight
                pair_liquidity = combined_weight_fraction * total_liquidity
                return pair_liquidity
            else:
                return 0.0
                
    except Exception as e:
        logger.error(f"Error calculating pair liquidity for {base_currency}-{target_currency} in {converter_name}: {e}")
        return 0.0

def test_liquidity_calculator():
    """Test the liquidity calculator with Bridge.vETH"""
    try:
        from data_integration import load_converter_data
        
        print("🧪 Testing Liquidity Calculator")
        print("=" * 50)
        
        # Load converter data
        converters_data = load_converter_data()
        if not converters_data:
            print("❌ No converter data available")
            return
        
        # Test with Bridge.vETH
        converter_name = "Bridge.vETH"
        
        # Test total converter liquidity
        total_liquidity = get_converter_liquidity(converter_name, converters_data)
        print(f"✅ Total {converter_name} liquidity: ${total_liquidity:.2f}")
        
        # Test pair liquidity for VRSC-DAI.vETH
        pair_liquidity = get_pair_liquidity(converter_name, "VRSC", "DAI.vETH", converters_data)
        print(f"✅ VRSC-DAI.vETH pair liquidity: ${pair_liquidity:.2f}")
        
        print("\n✅ Liquidity calculator test completed!")
        
    except Exception as e:
        print(f"❌ Error in liquidity calculator test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_liquidity_calculator()
