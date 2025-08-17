#!/usr/bin/env python3
"""
Working Validation Endpoint for Verus Ticker API
Based on comprehensive debugging results
"""

import json
from typing import Dict, Any, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkingAPIValidator:
    def __init__(self):
        self.results = {}
    
    def get_endpoint_data(self, endpoint: str) -> Tuple[Any, bool]:
        """Get data from endpoint using internal function calls with proper error handling"""
        try:
            if endpoint == "coingecko":
                from ticker_formatting import get_formatted_tickers
                result = get_formatted_tickers("coingecko")
                if isinstance(result, dict) and 'tickers' in result:
                    return result['tickers'], True
                elif 'error' in result:
                    logger.error(f"CoinGecko non-cached error: {result['error']}")
                    return [], False
                return [], False
            elif endpoint == "coingecko_cached":
                from ticker_formatting_cached import get_formatted_tickers_cached
                result = get_formatted_tickers_cached("coingecko")
                if isinstance(result, dict) and 'tickers' in result:
                    return result['tickers'], True
                return [], False
            elif endpoint == "coinmarketcap":
                from ticker_formatting import generate_coinmarketcap_enhanced_tickers
                from data_integration import extract_all_pairs_data
                pairs_result = extract_all_pairs_data()
                pairs_data = pairs_result.get('pairs', [])
                result = generate_coinmarketcap_enhanced_tickers(pairs_data)
                return result, True
            elif endpoint == "coinmarketcap_cached":
                from ticker_formatting_cached import get_clean_coinmarketcap_enhanced_tickers_cached
                result = get_clean_coinmarketcap_enhanced_tickers_cached()
                if isinstance(result, dict) and len(result) > 0:
                    return result, True
                return {}, False
            elif endpoint == "coinpaprika":
                from alltickers_formatter import generate_alltickers_response
                result = generate_alltickers_response()
                return result, True
            elif endpoint == "coinpaprika_cached":
                from alltickers_formatter import generate_alltickers_response_cached
                result = generate_alltickers_response_cached()
                return result, True
            else:
                return {"error": f"Unknown endpoint: {endpoint}"}, False
        except Exception as e:
            logger.error(f"Failed to get data for {endpoint}: {e}")
            return {"error": str(e)}, False
    
    def count_pairs(self, data: Any, endpoint_name: str) -> int:
        """Count pairs in endpoint data with proper structure handling"""
        try:
            if endpoint_name.startswith("coinpaprika"):
                # Coinpaprika format: JSON array [...]
                if isinstance(data, list):
                    return len(data)
                # Fallback for old format: {"data": {"ticker": [...]}}
                elif isinstance(data, dict) and 'data' in data and 'ticker' in data['data']:
                    return len(data['data']['ticker'])
            elif endpoint_name.startswith("coinmarketcap"):
                # CoinMarketCap format: dictionary of tickers
                if isinstance(data, dict):
                    return len(data)
                elif isinstance(data, list):
                    return len(data)
            else:
                # CoinGecko format: array of tickers
                if isinstance(data, list):
                    return len(data)
        except Exception as e:
            logger.error(f"Error counting pairs for {endpoint_name}: {e}")
        return 0
    
    def validate_pair_counts(self) -> Dict[str, Any]:
        """Validate pair counts across all endpoints"""
        endpoints = {
            "coingecko": "coingecko",
            "coingecko_cached": "coingecko_cached",
            "coinmarketcap": "coinmarketcap", 
            "coinmarketcap_cached": "coinmarketcap_cached",
            "coinpaprika": "coinpaprika",
            "coinpaprika_cached": "coinpaprika_cached"
        }
        
        pair_counts = {}
        for name, endpoint in endpoints.items():
            data, success = self.get_endpoint_data(endpoint)
            if success:
                pair_counts[name] = self.count_pairs(data, name)
            else:
                pair_counts[name] = 0
        
        # Compare cached vs non-cached for all endpoints
        comparisons = {
            "coingecko_vs_coingecko_cached": {
                "non_cached_count": pair_counts.get("coingecko", 0),
                "cached_count": pair_counts.get("coingecko_cached", 0),
                "match": pair_counts.get("coingecko", 0) == pair_counts.get("coingecko_cached", 0),
                "status": "PASS" if pair_counts.get("coingecko", 0) == pair_counts.get("coingecko_cached", 0) else "FAIL"
            },
            "coinmarketcap_vs_coinmarketcap_cached": {
                "non_cached_count": pair_counts.get("coinmarketcap", 0),
                "cached_count": pair_counts.get("coinmarketcap_cached", 0),
                "match": pair_counts.get("coinmarketcap", 0) == pair_counts.get("coinmarketcap_cached", 0),
                "status": "PASS" if pair_counts.get("coinmarketcap", 0) == pair_counts.get("coinmarketcap_cached", 0) else "FAIL"
            },
            "coinpaprika_vs_coinpaprika_cached": {
                "non_cached_count": pair_counts.get("coinpaprika", 0),
                "cached_count": pair_counts.get("coinpaprika_cached", 0),
                "match": pair_counts.get("coinpaprika", 0) == pair_counts.get("coinpaprika_cached", 0),
                "status": "PASS" if pair_counts.get("coinpaprika", 0) == pair_counts.get("coinpaprika_cached", 0) else "FAIL"
            }
        }
        
        return {
            "pair_counts": pair_counts,
            "cached_vs_non_cached": comparisons,
            "expected_counts": {
                "coingecko_cached": "64 (individual converter instances)",
                "coinmarketcap": "41 (aggregated unique pairs)",
                "coinpaprika": "41 (aggregated unique pairs)"
            }
        }
    
    def calculate_vrsc_base_volume(self, data: Any, endpoint_name: str) -> float:
        """Calculate total volume for all VRSC base pairs"""
        total_vrsc_volume = 0.0
        
        try:
            if endpoint_name.startswith("coinpaprika"):
                # Coinpaprika format: JSON array [...]
                if isinstance(data, list):
                    for ticker in data:
                        # Check if this is a VRSC base pair (symbol starts with VRSC-)
                        symbol = ticker.get('symbol', '')
                        if symbol.startswith('VRSC-'):
                            volume = float(ticker.get('volume', 0))
                            total_vrsc_volume += volume
                # Fallback for old format: {"data": {"ticker": [...]}}
                elif isinstance(data, dict) and 'data' in data and 'ticker' in data['data']:
                    tickers = data['data']['ticker']
                    for ticker in tickers:
                        # Check if this is a VRSC base pair (symbol starts with VRSC-)
                        symbol = ticker.get('symbol', '')
                        if symbol.startswith('VRSC-'):
                            volume = float(ticker.get('volume', 0))
                            total_vrsc_volume += volume
            elif endpoint_name.startswith("coinmarketcap"):
                # CoinMarketCap format: dictionary of tickers
                if isinstance(data, dict):
                    for ticker_key, ticker_data in data.items():
                        # Check if this is a VRSC base pair
                        base_symbol = ticker_data.get('base_symbol', '')
                        if base_symbol == 'VRSC':
                            volume = float(ticker_data.get('base_volume', 0))
                            total_vrsc_volume += volume
            else:
                # CoinGecko format: array of tickers
                if isinstance(data, list):
                    for ticker in data:
                        # Check if this is a VRSC base pair
                        base_currency = ticker.get('base_currency', '')
                        if base_currency == 'VRSC':
                            volume = float(ticker.get('base_volume', 0))
                            total_vrsc_volume += volume
        except Exception as e:
            logger.error(f"Error calculating VRSC volume for {endpoint_name}: {e}")
        
        return total_vrsc_volume
    
    def validate_vrsc_base_volumes(self) -> Dict[str, Any]:
        """Validate VRSC base volumes across all endpoints"""
        endpoints = {
            "coingecko": "coingecko",
            "coingecko_cached": "coingecko_cached",
            "coinmarketcap": "coinmarketcap", 
            "coinmarketcap_cached": "coinmarketcap_cached",
            "coinpaprika": "coinpaprika",
            "coinpaprika_cached": "coinpaprika_cached"
        }
        
        vrsc_volumes = {}
        for name, endpoint in endpoints.items():
            data, success = self.get_endpoint_data(endpoint)
            if success:
                vrsc_volumes[name] = self.calculate_vrsc_base_volume(data, name)
            else:
                vrsc_volumes[name] = 0.0
        
        # Format volumes to 8 decimal places
        formatted_volumes = {k: f"{v:.8f}" for k, v in vrsc_volumes.items()}
        
        # Check if volumes are reasonably close (within 5% tolerance for timing differences)
        volumes_list = [v for v in vrsc_volumes.values() if v > 0]
        volume_match_status = "INSUFFICIENT_DATA"
        
        if len(volumes_list) >= 2:
            max_vol = max(volumes_list)
            min_vol = min(volumes_list)
            if max_vol > 0:
                diff_percentage = (max_vol - min_vol) / max_vol * 100
                if diff_percentage <= 5.0:  # 5% tolerance
                    volume_match_status = "PASS"
                else:
                    volume_match_status = "FAIL"
        
        return {
            "vrsc_base_volumes": formatted_volumes,
            "volume_differences": {
                "max_volume": f"{max(volumes_list):.8f}" if volumes_list else "0.00000000",
                "min_volume": f"{min(volumes_list):.8f}" if volumes_list else "0.00000000",
                "difference_percentage": f"{((max(volumes_list) - min(volumes_list)) / max(volumes_list) * 100):.2f}%" if volumes_list and max(volumes_list) > 0 else "0.00%"
            },
            "vrsc_volume_match_status": volume_match_status
        }
    
    def run_validation(self) -> Dict[str, Any]:
        """Run validation and return results"""
        logger.info("🔍 Starting API validation...")
        
        # Validate pair counts
        pair_count_results = self.validate_pair_counts()
        
        # Validate VRSC base volumes
        vrsc_volume_results = self.validate_vrsc_base_volumes()
        
        # Determine overall status
        all_pairs_match = all(comparison["status"] == "PASS" for comparison in pair_count_results["cached_vs_non_cached"].values())
        vrsc_volumes_match = vrsc_volume_results["vrsc_volume_match_status"] == "PASS"
        
        overall_status = "PASS" if all_pairs_match and vrsc_volumes_match else "FAIL"
        
        # Build final results
        self.results = {
            "validation_summary": {
                "pair_count_validation": "PASS" if all_pairs_match else "FAIL",
                "vrsc_volume_validation": vrsc_volume_results["vrsc_volume_match_status"],
                "overall_status": overall_status
            },
            "detailed_results": {
                "pair_counts": pair_count_results,
                "vrsc_base_volume_analysis": vrsc_volume_results
            },
            "overall_status": overall_status
        }
        
        logger.info(f"✅ Validation complete. Overall status: {overall_status}")
        logger.info(f"📊 VRSC base volume validation: {vrsc_volume_results['vrsc_volume_match_status']}")
        return self.results

def run_validation() -> Dict[str, Any]:
    """Main function to run validation and return results"""
    validator = WorkingAPIValidator()
    return validator.run_validation()

if __name__ == "__main__":
    result = run_validation()
    print(json.dumps(result, indent=2))
