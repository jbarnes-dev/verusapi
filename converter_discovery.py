#!/usr/bin/env python3
"""
Converter Discovery Module
Discovers all active converters while respecting exclusion rules
"""

import json
from verus_rpc import make_verus_rpc
from dict import excluded_chains, get_ticker_by_id
from block_height import get_session_block_height

def get_all_converters(system_id="VRSC"):
    """
    Get all currency converters for a given system ID
    
    Args:
        system_id (str): The system ID to get converters for. Default is "VRSC"
        
    Returns:
        dict: The parsed response with converter information, or None if failed
    """
    try:
        print(f"🔄 Fetching all converters for system: {system_id}")
        
        # Get current session block height for consistency
        block_height = get_session_block_height()
        if block_height is None:
            print("❌ Cannot get converters without block height")
            return None
        
        # Make RPC call to get currency converters
        result = make_verus_rpc('getcurrencyconverters', [system_id])
        
        if result:
            print(f"✅ Successfully fetched {len(result)} converters at block {block_height}")
            return result
        else:
            print("❌ Failed to get currency converters")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching converters: {e}")
        return None

def filter_converters(converters_data):
    """
    Filter converters to exclude problematic ones based on exclusion rules
    
    Args:
        converters_data (list): Raw converter data from RPC call
        
    Returns:
        tuple: (filtered_converters, excluded_converters)
    """
    if not converters_data:
        return [], []
    
    filtered_converters = []
    excluded_converters = []
    
    print(f"🔄 Filtering converters (excluding: {excluded_chains})")
    
    for converter in converters_data:
        if 'fullyqualifiedname' in converter:
            converter_name = converter['fullyqualifiedname']
            
            # Check if this converter should be excluded
            if converter_name in excluded_chains:
                excluded_converters.append(converter)
                print(f"❌ Excluded converter: {converter_name}")
            else:
                filtered_converters.append(converter)
                print(f"✅ Included converter: {converter_name}")
        else:
            print(f"⚠️  Converter missing fullyqualifiedname: {converter}")
    
    print(f"🎯 Filter results: {len(filtered_converters)} included, {len(excluded_converters)} excluded")
    return filtered_converters, excluded_converters

def extract_converter_info(converter):
    """
    Extract key information from a converter
    
    Args:
        converter (dict): Single converter data from RPC response
        
    Returns:
        dict: Extracted converter information
    """
    info = {
        'name': None,
        'currency_id': None,
        'supply': None,
        'reserve_currencies': [],
        'raw_data': converter
    }
    
    try:
        # Get basic info
        if 'fullyqualifiedname' in converter:
            info['name'] = converter['fullyqualifiedname']
        
        # Extract currency ID from the converter keys
        for key in converter.keys():
            if key not in ['fullyqualifiedname', 'height', 'output', 'lastnotarization']:
                info['currency_id'] = key
                break
        
        # Extract detailed info from lastnotarization
        if 'lastnotarization' in converter and 'currencystate' in converter['lastnotarization']:
            currency_state = converter['lastnotarization']['currencystate']
            
            # Get supply
            if 'supply' in currency_state:
                info['supply'] = float(currency_state['supply'])
            
            # Get reserve currencies
            if 'reservecurrencies' in currency_state:
                for rc in currency_state['reservecurrencies']:
                    reserve_info = {
                        'currency_id': rc.get('currencyid', ''),
                        'ticker': get_ticker_by_id(rc.get('currencyid', '')),
                        'weight': float(rc.get('weight', 0)),
                        'reserves': float(rc.get('reserves', 0)),
                        'price_in_reserve': float(rc.get('priceinreserve', 0))
                    }
                    info['reserve_currencies'].append(reserve_info)
        
    except Exception as e:
        print(f"⚠️  Error extracting info from converter {info.get('name', 'unknown')}: {e}")
    
    return info

def discover_active_converters():
    """
    Main function to discover all active converters with filtering and info extraction
    
    Returns:
        dict: {
            'active_converters': list of filtered converter info,
            'excluded_converters': list of excluded converter info,
            'total_count': total converters found,
            'active_count': active converters after filtering,
            'excluded_count': excluded converters count,
            'block_height': block height used for this discovery
        }
    """
    print("🔍 Starting converter discovery process...")
    
    # Get current block height for this session
    block_height = get_session_block_height()
    
    # Get all converters
    raw_converters = get_all_converters()
    if not raw_converters:
        return {
            'active_converters': [],
            'excluded_converters': [],
            'total_count': 0,
            'active_count': 0,
            'excluded_count': 0,
            'block_height': block_height,
            'error': 'Failed to fetch converters'
        }
    
    # Filter converters
    filtered_converters, excluded_converters = filter_converters(raw_converters)
    
    # Extract detailed info for active converters
    active_converter_info = []
    for converter in filtered_converters:
        info = extract_converter_info(converter)
        active_converter_info.append(info)
    
    # Extract info for excluded converters (for reference)
    excluded_converter_info = []
    for converter in excluded_converters:
        info = extract_converter_info(converter)
        excluded_converter_info.append(info)
    
    result = {
        'active_converters': active_converter_info,
        'excluded_converters': excluded_converter_info,
        'total_count': len(raw_converters),
        'active_count': len(active_converter_info),
        'excluded_count': len(excluded_converter_info),
        'block_height': block_height
    }
    
    print(f"✅ Converter discovery complete:")
    print(f"   Total found: {result['total_count']}")
    print(f"   Active (included): {result['active_count']}")
    print(f"   Excluded: {result['excluded_count']}")
    print(f"   Block height: {result['block_height']}")
    
    # Automatically save the results to JSON file
    save_success = save_converter_discovery(result)
    if save_success:
        print(f"💾 Results saved to converter_discovery.json")
    else:
        print(f"❌ Failed to save results to converter_discovery.json")
    
    return result

def save_converter_discovery(discovery_result, filename="converter_discovery.json"):
    """
    Save converter discovery results to a JSON file
    
    Args:
        discovery_result (dict): Result from discover_active_converters()
        filename (str): Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(discovery_result, f, indent=2, default=str)
        print(f"💾 Converter discovery saved to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving converter discovery: {e}")
        return False

if __name__ == "__main__":
    # Test the converter discovery functionality
    print("🧪 Testing Converter Discovery Module")
    print("=" * 50)
    
    # Import session management for testing
    from block_height import start_new_session, clear_session
    
    # Start a new session
    session_id = start_new_session()
    
    try:
        # Discover active converters
        discovery = discover_active_converters()
        
        # Display summary
        print(f"\n📊 Discovery Summary:")
        print(f"Block Height: {discovery['block_height']}")
        print(f"Total Converters: {discovery['total_count']}")
        print(f"Active Converters: {discovery['active_count']}")
        print(f"Excluded Converters: {discovery['excluded_count']}")
        
        # Display active converters
        print(f"\n✅ Active Converters:")
        for converter in discovery['active_converters']:
            print(f"  - {converter['name']} ({len(converter['reserve_currencies'])} reserves)")
        
        # Display excluded converters
        print(f"\n❌ Excluded Converters:")
        for converter in discovery['excluded_converters']:
            print(f"  - {converter['name']}")
        
        # Save results
        save_converter_discovery(discovery)
        
    finally:
        # Clear session
        clear_session()
    
    print("✅ Converter discovery test complete")
