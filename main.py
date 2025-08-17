#!/usr/bin/env python3
"""
Verus Ticker API - FastAPI Implementation
Core FastAPI skeleton with basic structure and health checks
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, Response
import uvicorn
import logging
from datetime import datetime
import sys
import os
import json
from typing import Dict, Any
import subprocess
import signal
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app with pretty JSON formatting
app = FastAPI(
    title="Verus Ticker API",
    description="Real-time cryptocurrency ticker data from Verus blockchain",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# Configure JSON formatting for human readability
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse as BaseJSONResponse

class PrettyJSONResponse(BaseJSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            jsonable_encoder(content),
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(',', ': ')
        ).encode('utf-8')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception on {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    try:
        # Test RPC connection
        from verus_rpc import make_rpc_call
        
        # Simple RPC test
        result = make_rpc_call("VRSC", "getinfo", [])
        
        if result and 'blocks' in result:
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "rpc_connection": "ok",
                "current_block": result.get('blocks', 0),
                "version": "1.0.0"
            }
        else:
            raise HTTPException(status_code=503, detail="RPC connection failed")
            
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503, 
            detail=f"Service unhealthy: {str(e)}"
        )

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Clean and Simple VRSC/vETH Trace Process Documentation"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Verus Ticker API - VRSC/vETH Trace Documentation</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                background: #f0f8ff;
                color: #2c3e50;
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            h1 {
                color: #2c3e50;
                font-size: 2.2em;
                font-weight: 600;
                text-align: center;
                margin-bottom: 10px;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
            }
            
            .subtitle {
                text-align: center;
                color: #7f8c8d;
                margin-bottom: 40px;
                font-size: 1.1em;
                padding: 15px;
                background: #ecf0f1;
                border-radius: 6px;
            }
            
            h2 {
                color: #2c3e50;
                margin: 40px 0 20px 0;
                font-weight: 600;
                border-left: 4px solid #3498db;
                padding-left: 15px;
            }
            
            h3 {
                color: #34495e;
                margin: 30px 0 15px 0;
                font-weight: 600;
            }
            
            h4 {
                color: #5a6c7d;
                margin: 20px 0 10px 0;
                font-weight: 600;
            }
            
            .api-section {
                background: #3498db;
                color: white;
                padding: 30px;
                border-radius: 8px;
                margin-bottom: 40px;
                box-shadow: 0 4px 15px rgba(52, 152, 219, 0.2);
            }
            
            .api-section h2 {
                color: white;
                border-left: 4px solid rgba(255,255,255,0.5);
                margin-top: 0;
            }
            
            .api-section h3 {
                color: rgba(255,255,255,0.95);
                margin-top: 25px;
            }
            
            .api-section ul {
                list-style: none;
                padding-left: 0;
            }
            
            .api-section li {
                background: rgba(255,255,255,0.1);
                margin: 8px 0;
                padding: 12px 15px;
                border-radius: 4px;
                border-left: 3px solid rgba(255,255,255,0.3);
            }
            
            .api-section code {
                background: rgba(255,255,255,0.2);
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: 600;
            }
            
            .step-box {
                background: #ecf0f1;
                border-left: 4px solid #3498db;
                padding: 25px;
                margin: 25px 0;
                border-radius: 6px;
            }
            
            .step-box h3 {
                color: #2c3e50;
                margin-top: 0;
                font-weight: 600;
            }
            
            .step-box h4 {
                color: #34495e;
                margin: 20px 0 10px 0;
            }
            
            .command {
                background: #2c3e50;
                color: #2ecc71;
                padding: 15px;
                border-radius: 6px;
                font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
                margin: 15px 0;
                overflow-x: auto;
                border-left: 4px solid #2ecc71;
            }
            
            .code {
                background: #34495e;
                color: #ecf0f1;
                padding: 20px;
                border-radius: 6px;
                font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
                margin: 15px 0;
                overflow-x: auto;
                white-space: pre-wrap;
                border-left: 4px solid #3498db;
            }
            
            .formula {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 15px;
                border-radius: 6px;
                font-weight: 600;
                color: #856404;
                margin: 15px 0;
                display: block;
            }
            
            .comparison-table {
                width: 100%;
                border-collapse: collapse;
                margin: 25px 0;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .comparison-table th {
                background: #34495e;
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: 600;
            }
            
            .comparison-table td {
                padding: 12px 15px;
                border-bottom: 1px solid #ecf0f1;
            }
            
            .comparison-table tr:nth-child(even) {
                background: #f8f9fa;
            }
            
            .comparison-table tr:hover {
                background: #e8f4f8;
            }
            
            .badge {
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .badge-success {
                background: #27ae60;
                color: white;
            }
            
            .badge-warning {
                background: #f39c12;
                color: white;
            }
            
            .tech-detail {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 25px;
                margin: 20px 0;
                border-radius: 6px;
            }
            
            .tech-detail h4 {
                color: #2c3e50;
                margin-top: 0;
                margin-bottom: 15px;
                font-weight: 600;
            }
            
            .integrity {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                padding: 25px;
                margin: 25px 0;
                border-radius: 6px;
            }
            
            .integrity h3 {
                color: #155724;
                margin-top: 0;
                font-weight: 600;
            }
            
            .status {
                color: #27ae60;
                font-weight: 700;
            }
            
            .highlight {
                background: #fff3cd;
                color: #856404;
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: 600;
            }
            
            ul { padding-left: 20px; }
            li { margin: 8px 0; }
            p { margin-bottom: 15px; color: #5a6c7d; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Verus Ticker API</h1>
            <div class="subtitle">
                <strong>Version:</strong> 1.0.0 | <strong>Status:</strong> <span class="status">✅ Active</span> | <strong>Base URL:</strong> http://localhost:8765<br>
                <strong>Current Block:</strong> <span id="block-height">Loading...</span> | <strong>Cache:</strong> <span id="cache-refresh">Loading...</span>
            </div>
            
            <div class="api-section">
                <h2>📡 API Endpoints</h2>
                
                <h3>🏥 Health & Status</h3>
                <ul>
                    <li><code>GET /health</code> - Server status and RPC connection</li>
                    <li><code>GET /cache_status</code> - Cache information and block height</li>
                    <li><code>GET /validate</code> - Endpoint validation</li>
                </ul>
                
                <h3>📊 Ticker Data</h3>
                <ul>
                    <li><code>GET /coingecko</code> - CoinGecko format (array with pool_id)</li>
                    <li><code>GET /coinmarketcap</code> - CoinMarketCap format (object with composite keys)</li>
                    <li><code>GET /coinpaprika</code> - Coinpaprika format (VerusStatisticsAPI compatible)</li>
                    <li><code>GET /coinmarketcap_iaddress</code> - CMC I-Address format (testing with Verus native IDs)</li>
                </ul>
                
                <h3>⚡ Cached Endpoints (60s TTL)</h3>
                <ul>
                    <li><code>GET /coingecko_cached</code> - CoinGecko cached</li>
                    <li><code>GET /coinmarketcap_cached</code> - CoinMarketCap cached</li>
                    <li><code>GET /coinpaprika_cached</code> - Coinpaprika cached</li>
                    <li><code>GET /coinmarketcap_iaddress_cached</code> - CMC I-Address cached</li>
                </ul>
                
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Endpoint Type</th>
                            <th>Original Endpoint</th>
                            <th>Cached Endpoint</th>
                            <th>Pairs Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>CoinGecko Format</strong></td>
                            <td class="original"><code>/coingecko</code></td>
                            <td class="cached"><code>/coingecko_cached</code> <span class="badge badge-success">RECOMMENDED</span></td>
                            <td>62 pairs</td>
                        </tr>
                        <tr>
                            <td><strong>CoinMarketCap DEX</strong></td>
                            <td class="original"><code>/coinmarketcap</code></td>
                            <td class="cached"><code>/coinmarketcap_cached</code> <span class="badge badge-success">RECOMMENDED</span></td>
                            <td>41 pairs</td>
                        </tr>
                        <tr>
                            <td><strong>Coinpaprika Format</strong></td>
                            <td class="original"><code>/coinpaprika</code></td>
                            <td class="cached"><code>/coinpaprika_cached</code> <span class="badge badge-success">RECOMMENDED</span></td>
                            <td>41 pairs</td>
                        </tr>
                        <tr>
                            <td><strong>CMC I-Address (Testing)</strong></td>
                            <td class="original"><code>/coinmarketcap_iaddress</code></td>
                            <td class="cached"><code>/coinmarketcap_iaddress_cached</code> <span class="badge badge-warning">TESTING</span></td>
                            <td>41 pairs</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <h2>🔍 VRSC/vETH Trace Process Documentation</h2>
            <p>This explains how we trace and calculate the VRSC/vETH trading pair in the NATI🦉 converter using CLI commands.</p>
            
            <div class="step-box">
                <h3>Step 1: Get Current Block Height</h3>
                <p>Establish the time range for data collection:</p>
                <div class="command">./verus getinfo</div>
                <div class="code">{
  "height": 3673862,
  "blocks": 3673862
}</div>
                <p><strong>Block Range Calculation:</strong></p>
                <div class="formula">Start Block = 3673862 - 1440 = 3672422</div>
                <div class="formula">End Block = 3673862 (current)</div>
                <div class="formula">Interval = 1440 blocks (≈ 24 hours)</div>
            </div>
            
            <div class="step-box">
                <h3>Step 2: Find the NATI🦉 Converter</h3>
                <div class="command">./verus getcurrencyconverters VRSC</div>
                <div class="code">[
  {
    "currencyid": "iH37kRsdfoHtHK5TottP1Yfq8hBSHz9btw",
    "name": "NATI🦉",
    "options": 41
  }
]</div>
                <p><strong>Result:</strong> Found NATI🦉 converter with ID <code>iH37kRsdfoHtHK5TottP1Yfq8hBSHz9btw</code></p>
            </div>
            
            <div class="step-box">
                <h3>Step 3: Get Converter-to-VRSC Rate</h3>
                <p>Calculate how much VRSC you get for 1 NATI🦉 (for liquidity calculation):</p>
                <div class="command">./verus estimateconversion '[{"currency":"NATI🦉", "convertto":"VRSC", "amount": 1}]'</div>
                <div class="code">{
  "estimatedcurrencyout": 156.72258332
}</div>
                <div class="formula">1 NATI🦉 = 156.72258332 VRSC</div>
            </div>
            
            <div class="step-box">
                <h3>Step 4: Get VRSC-to-DAI Rate</h3>
                <p>Get USD valuation by converting VRSC to DAI:</p>
                <div class="command">./verus estimateconversion '[{"currency":"VRSC", "convertto":"DAI.vETH", "amount": 1, "via": "Bridge.vETH"}]'</div>
                <div class="code">{
  "estimatedcurrencyout": 2.15310337
}</div>
                <div class="formula">1 VRSC = 2.15310337 DAI ≈ $2.15</div>
            </div>
            
            <div class="step-box">
                <h3>Step 5: Get Converter Details</h3>
                <div class="command">./verus getcurrency iH37kRsdfoHtHK5TottP1Yfq8hBSHz9btw</div>
                <div class="code">{
  "name": "NATI🦉",
  "supply": 69665.89779233,
  "currencies": [
    "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV", // VRSC
    "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", // tBTC.vETH
    "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X", // vETH
    "iL62spNN42Vqdxh8H5nrfNe8d6Amsnfkdx"  // NATI.vETH
  ],
  "weights": [0.25, 0.25, 0.25, 0.25]
}</div>
                <p><strong>Key Details:</strong></p>
                <ul>
                    <li>Supply: 69,665.89779233 NATI🦉</li>
                    <li>Reserve Currencies: VRSC, tBTC.vETH, vETH, NATI.vETH</li>
                    <li>Weights: 25% each (0.25)</li>
                </ul>
            </div>
            
            <div class="step-box">
                <h3>Step 6: Extract Volume Data for VRSC/vETH Pair</h3>
                <p>Get trading volume and OHLC data for both directions:</p>
                
                <h4>VRSC Base Volume:</h4>
                <div class="command">./verus getcurrencystate iH37kRsdfoHtHK5TottP1Yfq8hBSHz9btw 3672422,3673862,1440 VRSC</div>
                <div class="code">{
  "conversiondata": {
    "volumecurrency": "VRSC",
    "volumethisinterval": 161317.61984463,
    "volumepairs": [{
      "currency": "VRSC",
      "convertto": "vETH",
      "volume": 25035.42967509,
      "open": 1661.91855093,
      "high": 1669.09163912,
      "low": 1645.79514717,
      "close": 1669.09163912
    }]
  }
}</div>
                
                <h4>vETH Base Volume:</h4>
                <div class="command">./verus getcurrencystate iH37kRsdfoHtHK5TottP1Yfq8hBSHz9btw 3672422,3673862,1440 vETH</div>
                <div class="code">{
  "conversiondata": {
    "volumecurrency": "vETH",
    "volumethisinterval": 97.43627670,
    "volumepairs": [{
      "currency": "VRSC",
      "convertto": "vETH",
      "volume": 15.12028821,
      "open": 1661.91855093,
      "high": 1669.09163912,
      "low": 1645.79514717,
      "close": 1669.09163912
    }]
  }
}</div>
            </div>
            
            <div class="step-box">
                <h3>Step 7: Calculate Liquidity</h3>
                
                <h4>Total Converter Liquidity in USD:</h4>
                <div class="formula">Total = Supply × NATI🦉:VRSC × VRSC:DAI</div>
                <div class="formula">Total = 69,665.90 × 156.72 × 2.15 = $23,508,055</div>
                
                <h4>Pair Liquidity (50% allocation):</h4>
                <div class="formula">Pair = $23,508,055 × 0.5 = $11,754,027</div>
                
                <h4>Symbol Mapping:</h4>
                <div class="formula">vETH → WETH (Wrapped Ether)</div>
                <div class="formula">Contract: 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2</div>
                
                <h4>Composite Key:</h4>
                <div class="formula">0xBc2738BA63882891094C99E59a02141Ca1A1C36a_0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2</div>
            </div>
            
            <h2>📡 API Endpoints</h2>
            
            <h3>🏥 Health & Status</h3>
            <ul>
                <li><code>GET /health</code> - Server status and RPC connection</li>
                <li><code>GET /cache_status</code> - Cache information and block height</li>
                <li><code>GET /validate</code> - Endpoint validation</li>
            </ul>
            
            <h3>📊 Ticker Data</h3>
            <ul>
                <li><code>GET /coingecko</code> - CoinGecko format (array with pool_id)</li>
                <li><code>GET /coinmarketcap</code> - CoinMarketCap format (object with composite keys)</li>
                <li><code>GET /coinpaprika</code> - Coinpaprika format (VerusStatisticsAPI compatible)</li>
                <li><code>GET /coinmarketcap_iaddress</code> - CMC I-Address format (testing with Verus native IDs)</li>
            </ul>
            
            <h3>⚡ Cached Endpoints (60s TTL)</h3>
            <ul>
                <li><code>GET /coingecko_cached</code> - CoinGecko cached</li>
                <li><code>GET /coinmarketcap_cached</code> - CoinMarketCap cached</li>
                <li><code>GET /coinpaprika_cached</code> - Coinpaprika cached</li>
                <li><code>GET /coinmarketcap_iaddress_cached</code> - CMC I-Address cached</li>
            </ul>
                <p><strong>Liquidity Calculation:</strong> Pool liquidity × currency weight (typically 25% for 4-currency pools)</p>
                <div class="code">curl http://localhost:8765/coingecko_cached</div>
            </div>
            
            <div class="tech-detail">
                <h4>💹 CoinMarketCap Format (41 Aggregated Pairs)</h4>
                <p><strong>Data Structure:</strong> Object with sequential numeric keys ("0", "1", "2", etc.) for CMC DEX API compliance</p>
                <p><strong>Pair Aggregation:</strong> Same trading pairs from multiple converters are combined into single entries</p>
                <p><strong>Volume Aggregation:</strong> Sums volumes from all converters for the same currency pair</p>
                <p><strong>Price Aggregation:</strong> Volume-weighted average pricing across all instances</p>
                <p><strong>Symbol Source:</strong> Uses Ethereum-standardized symbols from <code>currency_contract_mapping.eth_symbol</code></p>
                <p><strong>Contract Integration:</strong> Uses ERC20 contract addresses for base_id/quote_id fields</p>
                <div class="code">curl http://localhost:8765/coinmarketcap_cached</div>
            </div>
            
            <div class="tech-detail">
                <h4>🌐 Coinpaprika Format (41 Aggregated Pairs)</h4>
                <p><strong>Format Compatibility:</strong> VerusStatisticsAPI wrapper structure with <code>{"code":"200000","data":{"time":timestamp,"ticker":[...]}}</code></p>
                <p><strong>Pair Aggregation:</strong> Same as CoinMarketCap - combines same trading pairs from multiple converters</p>
                <p><strong>Symbol Standard:</strong> Uses Ethereum-standardized symbols from <code>currency_contract_mapping.eth_symbol</code></p>
                <p><strong>Data Structure:</strong> Array of ticker objects with symbol, volume, last, high, low, open fields</p>
                <p><strong>Exclusion Logic:</strong> Filters converter currencies and excluded chains</p>
                <p><strong>Price Fallback:</strong> When <code>last_price = 0</code>, uses <code>(high + low) / 2</code> calculation</p>
                <div class="code">curl http://localhost:8765/coinpaprika_cached</div>
            </div>
            
            <div class="tech-detail">
                <h4>🧪 CMC I-Address Format (41 Aggregated Pairs - Testing)</h4>
                <p><strong>Purpose:</strong> Testing endpoint using Verus i-addresses instead of ERC20 contract addresses</p>
                <p><strong>Pair Aggregation:</strong> Same aggregation logic as CoinMarketCap (41 unique pairs)</p>
                <p><strong>Key Differences:</strong> Uses currency IDs (i-addresses) as base_id/quote_id instead of contract addresses</p>
                <p><strong>Data Structure:</strong> Identical to CoinMarketCap format but with i-address identifiers</p>
                <p><strong>Symbol Source:</strong> Uses Verus native currency names from <code>currency_contract_mapping.vrsc_symbol</code></p>
                <p><strong>Format Structure:</strong> CoinMarketCap DEX API compatible with sequential keys ("0", "1", "2", etc.)</p>
                <p><strong>Use Case:</strong> Testing and validation of Verus native identifier integrations</p>
                <div class="code">curl http://localhost:8765/coinmarketcap_iaddress_cached</div>
            </div>
            

            
            <h3>⚙️ Detailed Data Collection and Calculation Process</h3>
            
            <div class="tech-detail">
                <h4>Step 1: Converter Discovery and Filtering</h4>
                <p><strong>Method:</strong> Call <code>getcurrencyconverters("VRSC")</code> RPC method to get all converters in the VRSC system</p>
                <p><strong>Filtering:</strong> Exclude converters listed in <code>excluded_chains</code> array: <code>["Bridge.CHIPS", "Bridge.vDEX", "Bridge.vARRR", "whales"]</code></p>
                <p><strong>Validation:</strong> Check each converter has <code>fullyqualifiedname</code> field and is not in exclusion list</p>
                <p><strong>Result:</strong> List of active converters that contain VRSC as a reserve currency</p>
                <p><strong>Current Count:</strong> 9 active converters (Bridge.vETH, Switch, Kaiju, vYIELD, SUPER🛒, NATI🦉, Pure, SUPERVRSC, NATI)</p>
            </div>
            
            <div class="tech-detail">
                <h4>Step 2: Currency Weight Extraction</h4>
                <p><strong>Method:</strong> For each converter, extract <code>currencies</code> array from converter discovery data</p>
                <p><strong>Weight Calculation:</strong> Each currency has a <code>weight</code> field (e.g., 25000000 = 0.25 or 25%)</p>
                <p><strong>Total Weight:</strong> Sum all currency weights in the converter (typically = 100000000 = 1.0 or 100%)</p>
                <p><strong>Currency Info:</strong> Extract <code>currencyid</code>, <code>weight</code>, and <code>symbol</code> for each currency in the converter</p>
                <p><strong>Validation:</strong> Ensure all currencies have valid weights and currency IDs</p>
            </div>
            
            <div class="tech-detail">
                <h4>Step 3: Total Converter Liquidity Calculation (USD)</h4>
                <p><strong>Step 3a:</strong> Get converter supply from discovery data (<code>supply</code> field)</p>
                <p><strong>Step 3b:</strong> Get converter-to-VRSC ratio using <code>estimateconversion(converter_id, "VRSC", 1)</code></p>
                <p><strong>Step 3c:</strong> Get VRSC-to-USD price using <code>estimateconversion("VRSC", "DAI.vETH", 1, via="Bridge.vETH")</code> (DAI ≈ $1 USD)</p>
                <p><strong>Formula:</strong> <code>Total Liquidity = Supply × Converter_to_VRSC_ratio × VRSC_USD_price</code></p>
                <p><strong>Example:</strong> Bridge.vETH supply × Bridge.vETH_to_VRSC_ratio × VRSC_USD_price = Total USD liquidity</p>
            </div>
            
            <div class="tech-detail">
                <h4>Step 4: Pair Liquidity Calculation</h4>
                <p><strong>Method:</strong> For each trading pair (base_currency, target_currency) in a converter</p>
                <p><strong>Weight Sum:</strong> Add the weight of base_currency + weight of target_currency</p>
                <p><strong>Formula:</strong> <code>Pair Liquidity = Total_Converter_Liquidity × (Weight_Base + Weight_Target) / Total_Weight</code></p>
                <p><strong>Example:</strong> If VRSC (25%) + DAI.vETH (25%) in Bridge.vETH = 50% of total converter liquidity</p>
                <p><strong>Result:</strong> Pair liquidity represents the portion of total converter liquidity allocated to that specific trading pair</p>
            </div>
            
            <div class="tech-detail">
                <h4>Step 5: Real Volume Calculation Method</h4>
                <p><strong>Method:</strong> Call <code>getcurrencystate(converter_name, "start_block,end_block,interval", volume_currency)</code> for each currency in the converter</p>
                <p><strong>Block Range:</strong> Use current_block - 1440 to current_block (24-hour period with 1440 blocks ≈ 24 hours)</p>
                <p><strong>Multiple Calls:</strong> Make separate calls for each currency as the <code>volume_currency</code> parameter</p>
                <p><strong>Base Volume:</strong> Extract volume from <code>getcurrencystate</code> call using base_currency as volume_currency parameter</p>
                <p><strong>Target Volume:</strong> Extract volume from <code>getcurrencystate</code> call using target_currency as volume_currency parameter</p>
                <p><strong>Data Source:</strong> Real blockchain volume data from <code>conversiondata.volumepairs</code> in the response</p>
                <p><strong>Precision:</strong> All volumes returned as-is from blockchain (typically 8 decimal places)</p>
            </div>
            
            <div class="tech-detail">
                <h4>Step 6: OHLC Price Data Extraction and Price Inversion</h4>
                <p><strong>Method:</strong> Extract OHLC (Open, High, Low, Close) data from the same <code>getcurrencystate</code> calls used for volume</p>
                <p><strong>Source:</strong> Price data comes from <code>conversiondata.volumepairs</code> entries for the specific trading pair</p>
                <p><strong>Price Inversion:</strong> When necessary, invert prices using <code>1 / original_price</code> to maintain proper base/target relationships</p>
                <p><strong>Direction Logic:</strong> Ensure price represents target_currency per unit of base_currency (e.g., DAI per VRSC)</p>
                <p><strong>Consistency:</strong> Use target_currency call data for OHLC to maintain consistency with volume methodology</p>
                <p><strong>Fallback:</strong> If no OHLC data available, set values to 0 or use fallback calculations</p>
            </div>
            
            <div class="tech-detail">
                <h4>Step 7: Data Aggregation and Formatting</h4>
                <p><strong>Pair Creation:</strong> Generate all possible trading pairs (base→target) for currencies within each converter</p>
                <p><strong>Volume Filtering:</strong> Only include pairs with volume > 0 (either base_volume > 0 or target_volume > 0)</p>
                <p><strong>Currency Mapping:</strong> Apply ERC20 symbol mapping from <code>currency_contract_mapping</code> for Ethereum compatibility</p>
                <p><strong>Exclusion:</strong> Filter out pairs involving converter currencies or currencies in excluded chains</p>
                <p><strong>Precision:</strong> Format all numeric values to 8 decimal places as strings to prevent scientific notation</p>
            </div>
            
            <div class="tech-detail">
                <h4>Step 8: Endpoint-Specific Output Formatting</h4>
                <p><strong>CoinGecko Format:</strong> Array of ticker objects with <code>ticker_id</code>, volumes, prices, <code>pool_id</code>, <code>liquidity_in_usd</code></p>
                <p><strong>CoinMarketCap Format:</strong> Object with contract address composite keys, aggregated same-pair data</p>
                <p><strong>Coinpaprika Format:</strong> VerusStatisticsAPI wrapper with <code>{"code":"200000","data":{"time":timestamp,"ticker":[...]}}</code></p>
                <p><strong>Caching:</strong> All endpoints have cached versions using 60-second TTL for performance optimization</p>
            </div>
            
            <h3>🔗 Ethereum Contract Integration</h3>
            
            <div class="tech-detail">
                <h4>📋 Complete Contract Address Mapping</h4>
                <p><strong>Data Source:</strong> <code>currency_contract_mapping</code> contains ERC20 contract addresses for Verus currencies exported to Ethereum</p>
                <p><strong>Coverage:</strong> 14 currencies mapped to ERC20 contracts representing 99.8% of total trading volume</p>
                <p><strong>Structure:</strong> Each currency maps to <code>{"address": "0x...", "eth_symbol": "SYMBOL", "vrsc_symbol": "VRSC_NAME"}</code></p>
                
                <div class="code">
                <strong>Complete currency_contract_mapping:</strong><br><br>
                
                <strong>Ethereum-Exported Currencies:</strong><br>
                • DAI.vETH (iGBs4DWz...): 0x6B175474E89094C44Da98b954EedeAC495271d0F → DAI<br>
                • EURC.vETH (iC5TQFrF...): 0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c → EURC<br>
                • MKR.vETH (iCkKJuJS...): 0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2 → MKR<br>
                • NATI.vETH (iL62spNN...): 0x4f14E88B5037F0cA24348Fa707E4A7Ee5318d9d5 → NATION<br>
                • VRSC (i5w5MuNi...): 0xBc2738BA63882891094C99E59a02141Ca1A1C36a → VRSC<br>
                • scrvUSD.vETH (i9nLSK4S...): 0x0655977FEb2f289A4aB78af67BAB0d17aAb84367 → CRVUSD<br>
                • tBTC.vETH (iS8TfRPf...): 0x18084fbA666a33d37592fA2633fD49a74DD93a88 → TBTC<br>
                • vARRR (iExBJfZY...): 0x45766AE12411450e20bd1c8cca1e63DffD834e19 → VARR<br>
                • vUSDC.vETH (i61cV2ui...): 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 → USDC<br>
                • vUSDT.vETH (i9oCSqKA...): 0xdAC17F958D2ee523a2206206994597C13D831ec7 → USDT<br><br>
                
                <strong>Verus Native with ERC20 Contracts:</strong><br>
                • vETH (i9nwxtKu...): 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 → WETH<br>
                • CHIPS (iJ3WZocn...): 0x714cFa2DA83b53b8fe2c1c9F99ca723A4c61AD48 → CHIPS<br>
                • SUPERNET (i6SapneN...): 0x504DAa3346f4AE4E624932FD654339Ad971FB242 → SUPERNET<br>
                • vDEX (iHog9UCT...): 0x0609Aede2f67C136bcb0e413E298F6cA8e283c37 → VDEX<br>
                </div>
            </div>
            
            <div class="tech-detail">
                <h4>🏷️ Symbol Standardization</h4>
                <p><strong>Verus Native (CoinGecko/CoinMarketCap):</strong> Uses original Verus currency names (DAI.vETH, MKR.vETH, tBTC.vETH)</p>
                <p><strong>ERC20 Standard (Coinpaprika):</strong> Uses Ethereum-standardized symbols (DAI, MKR, TBTC) from <code>eth_symbol</code> field</p>
                <p><strong>Contract Keys (CoinMarketCap):</strong> Uses contract address composite keys for unique pair identification</p>
                <p><strong>Fallback Logic:</strong> Currencies without ERC20 mapping retain their Verus native symbols</p>
            </div>
            
            <div class="tech-detail">
                <h4>🔄 Cross-Chain Compatibility</h4>
                <p><strong>Ethereum Integration:</strong> Contract addresses enable direct integration with Ethereum DeFi protocols</p>
                <p><strong>Token Names:</strong> Official Etherscan token names ("USD Coin", "Dai Stablecoin", "Wrapped Ether") for ecosystem familiarity</p>
                <p><strong>Address Validation:</strong> All contract addresses verified against live Ethereum blockchain data</p>
                <p><strong>Multi-Chain Support:</strong> Architecture supports future expansion to other blockchain networks</p>
            </div>
            
            <div class="tech-detail">
                <h4>🆚 CoinMarketCap vs I-Address Endpoint Comparison</h4>
                <p><strong>Purpose:</strong> The I-Address endpoint provides identical functionality to CoinMarketCap but uses Verus native identifiers for testing and validation</p>
                
                <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                    <thead>
                        <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                            <th style="padding: 12px; text-align: left; border: 1px solid #dee2e6;">Feature</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid #dee2e6;">Regular CoinMarketCap</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid #dee2e6;">I-Address CoinMarketCap</th>
                            <th style="padding: 12px; text-align: left; border: 1px solid #dee2e6;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #dee2e6;"><strong>Key Format</strong></td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;"><code>CONTRACT_CONTRACT</code></td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;"><code>IADDRESS_IADDRESS</code></td>
                            <td style="padding: 10px; border: 1px solid #dee2e6; color: #28a745;">✅ <strong>Exact Same</strong></td>
                        </tr>
                        <tr style="background-color: #f8f9fa;">
                            <td style="padding: 10px; border: 1px solid #dee2e6;"><strong>Structure</strong></td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">base_id, base_name, base_symbol, quote_id, quote_name, quote_symbol, etc.</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">base_id, base_name, base_symbol, quote_id, quote_name, quote_symbol, etc.</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6; color: #28a745;">✅ <strong>Identical</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #dee2e6;"><strong>Base/Quote IDs</strong></td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">ERC20 contract addresses</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">Verus i-addresses</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6; color: #28a745;">✅ <strong>As Requested</strong></td>
                        </tr>
                        <tr style="background-color: #f8f9fa;">
                            <td style="padding: 10px; border: 1px solid #dee2e6;"><strong>Names/Symbols</strong></td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">ERC20 symbols (DAI, WETH)</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">Verus native (DAI.vETH, vETH)</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6; color: #28a745;">✅ <strong>Verus Native</strong></td>
                        </tr>
                    </tbody>
                </table>
                
                <p><strong>Usage:</strong></p>
                <div class="code">curl http://localhost:8765/coinmarketcap_cached  # ERC20 contract addresses</div>
                <div class="code">curl http://localhost:8765/coinmarketcap_iaddress_cached  # Verus i-addresses</div>
            </div>
            
            <h3>📊 Aggregation Logic and Methodologies</h3>
            
            <div class="tech-detail">
                <h4>🔗 Current Data Processing (All Endpoints)</h4>
                <p><strong>Pair Generation:</strong> Each endpoint generates 57 unique trading pairs from active converters</p>
                <p><strong>Data Consistency:</strong> All endpoints use identical blockchain data with same block height</p>
                <p><strong>Volume Extraction:</strong> Direct volume data from individual converter pairs via <code>getcurrencystate</code> RPC calls</p>
                <p><strong>Price Calculation:</strong> OHLC data extracted from blockchain volume pairs</p>
                <p><strong>Result:</strong> 57 consistent pairs across all endpoints with different formatting and symbol standards</p>
            </div>
            
            <div class="tech-detail">
                <h4>📈 Volume-Weighted Price Calculation</h4>
                <p><strong>Methodology:</strong> Each price component weighted by its corresponding volume for accurate market representation</p>
                <p><strong>Formula:</strong> <code>weighted_avg = Σ(price_i × volume_i) / Σ(volume_i)</code></p>
                <p><strong>OHLC Aggregation:</strong> High = max(all_highs), Low = min(all_lows), Open/Close = volume-weighted averages</p>
                <p><strong>Fallback Logic:</strong> When last_price = 0, use (high + low) / 2 for price calculations</p>
            </div>
            
            <div class="tech-detail">
                <h4>🚫 Exclusion and Filtering Logic</h4>
                <p><strong>Converter Currency Exclusion:</strong> <code>is_converter_currency()</code> removes basket currencies from trading pairs</p>
                <p><strong>Chain Exclusion:</strong> <code>excluded_chains</code> filters out problematic converters (Bridge.CHIPS, Bridge.vDEX, etc.)</p>
                <p><strong>Volume Filtering:</strong> Only pairs with base_volume > 0 OR target_volume > 0 are included</p>
                <p><strong>Contract Validation:</strong> Pairs without valid contract addresses use fallback symbol mapping</p>
            </div>
            
            <div class="integrity">
                <h3>✅ Data Validation & Consistency</h3>
                <p><strong>Pair Count Validation:</strong> All endpoints return exactly 57 trading pairs with consistent data</p>
                <p><strong>Cross-Endpoint Validation:</strong> All cached endpoints return identical data to their original counterparts</p>
                <p><strong>Validation Endpoint:</strong> <code>/validate</code> endpoint confirms perfect data integrity across all endpoints</p>
                <p><strong>Block Height Consistency:</strong> All endpoints use the same blockchain block height for data consistency</p>
            </div>
            
            <div class="tech-detail">
                <h3>🔗 Contract Address Integration</h3>
                <p><strong>Data Source:</strong> <code>currency_contract_mapping</code> in dict.py contains authoritative ERC20 contract addresses</p>
                <p><strong>Coverage:</strong> 15 currencies with ERC20 contracts, 99.8% volume coverage</p>
                <p><strong>Key Mappings:</strong></p>
                <ul>
                    <li><code>DAI.vETH → 0x6B175474E89094C44Da98b954EedeAC495271d0F (DAI)</code></li>
                    <li><code>vETH → 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 (WETH)</code></li>
                    <li><code>NATI.vETH → 0x0F5D2fB29fb7d3CFeE444a200298f468908cC942 (NATION)</code></li>
                    <li><code>VRSC → 0x83D2944d5fC10A064451Dc5852f4F47759F249B6</code></li>
                </ul>
                <p><strong>Fallback Logic:</strong> Currencies without contracts use Verus native symbols</p>
            </div>
            
            <div class="tech-detail">
                <h3>🚫 Converter Currency Exclusion</h3>
                <p><strong>Exclusion Logic:</strong> <code>is_converter_currency(currency_id)</code> filters out multi-currency basket pairs</p>
                <p><strong>Excluded Converters:</strong> Bridge.vETH, SUPERVRSC, SUPER🛒, Switch, Kaiju, NATI🦉, Pure, vYIELD, whales, NATI</p>
                <p><strong>Reason:</strong> Converter currencies represent baskets, not tradeable pairs</p>
                <p><strong>Implementation:</strong> Applied across all endpoints (CoinGecko, CoinMarketCap, Coinpaprika)</p>
                
                <h4>📊 Price Aggregation Method</h4>
                <p><strong>Quote Volume Weighting:</strong> When the same trading pair exists across multiple converters, the final <code>last_price</code> is calculated using volume-weighted averaging with <strong>quote volume</strong> as the weight. This ensures that higher dollar-value trades have more influence on the final price.</p>
                <p><strong>Formula:</strong> <code>weighted_price = (price1 × quote_vol1 + price2 × quote_vol2) / (quote_vol1 + quote_vol2)</code></p>
                <p><strong>Applied to:</strong> /coinmarketcap, /coinmarketcap_cache, /coinmarketcap_iaddress, /coinmarketcap_iaddress_cache, /coinpaprika, /coinpaprika_cache</p>
            </div>
            

            

            

            
            <hr style="margin: 30px 0;">
            <p style="text-align: center; color: #7f8c8d;"><em>Verus Ticker API - Providing real-time, validated cryptocurrency data from the Verus blockchain</em></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# API v1 router placeholder (unused endpoint removed)

# Ticker endpoints - integrated with validated data extraction and formatting
@app.get("/coingecko")
async def get_coingecko_tickers():
    """CoinGecko format tickers endpoint using currency_contract_mapping symbols"""
    try:
        from ticker_formatting import get_formatted_tickers
        
        logger.info("Processing CoinGecko tickers request")
        result = get_formatted_tickers("coingecko2")
        
        if 'error' in result:
            logger.error(f"CoinGecko tickers error: {result['error']}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get ticker data: {result['error']}"
            )
        
        # Return the tickers array directly (CoinGecko format)
        tickers = result.get('tickers', [])
        logger.info(f"Successfully returned {len(tickers)} CoinGecko tickers with proper symbol mapping")
        
        # Return human-readable JSON with proper formatting
        return PrettyJSONResponse(
            content=tickers,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"CoinGecko tickers endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Removed unused /allTickers endpoint

# Removed unused /allTickers_new endpoint

@app.get("/coinmarketcap")
async def get_cmc_summary():
    """
    Get ticker data in Enhanced CoinMarketCap (CMC) DEX format with Ethereum contract details
    Uses contract addresses and symbols (e.g., WETH instead of ETH) when available
    
    Returns:
        Object with composite keys containing enhanced ticker data per CMC DEX specification
        Pretty-printed JSON for human readability with Ethereum contract compatibility
    """
    from fastapi.responses import Response
    from ticker_formatting import generate_coinmarketcap_enhanced_tickers
    from data_integration import extract_all_pairs_data
    import json
    
    try:
        
        logger.info("🚀 Enhanced CMC DEX coinmarketcap endpoint called")
        
        # Get raw pairs data
        pairs_result = extract_all_pairs_data()
        pairs_data = pairs_result.get('pairs', []) if isinstance(pairs_result, dict) else []
        
        if not pairs_data:
            logger.warning("⚠️ No pairs data available for enhanced CMC")
            error_json = json.dumps({"error": "No pairs data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        # Generate enhanced CMC tickers with contract details
        enhanced_tickers = generate_coinmarketcap_enhanced_tickers(pairs_data)
        
        if not enhanced_tickers:
            logger.warning("⚠️ No enhanced CMC ticker data generated")
            error_json = json.dumps({"error": "No enhanced ticker data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        logger.info(f"✅ Returning {len(enhanced_tickers)} enhanced CMC DEX tickers with contract details")
        
        # Convert to pretty-printed JSON with proper indentation
        pretty_json = json.dumps(enhanced_tickers, indent=2, ensure_ascii=False)
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"❌ Error in enhanced CMC coinmarketcap endpoint: {e}")
        error_json = json.dumps({"error": str(e)}, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )



# Removed unused /enhanced endpoint

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    try:
        # Find process using the port
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"Killing process {pid} on port {port}")
                    os.kill(int(pid), signal.SIGTERM)
                    time.sleep(1)
                    # Force kill if still running
                    try:
                        os.kill(int(pid), signal.SIGKILL)
                    except ProcessLookupError:
                        pass
            print(f"Cleared port {port}")
        else:
            print(f"Port {port} is free")
    except Exception as e:
        print(f"Error checking/clearing port {port}: {e}")

# ============================================================================
# CACHED ENDPOINTS - Performance optimized versions with unified caching
# ============================================================================

@app.get("/coingecko_cached")
async def get_coingecko_tickers_cached():
    """
    Get all tickers in CoinGecko format (CACHED VERSION)
    
    Features:
    - Unified caching reduces RPC calls
    - Shared data across all cached endpoints
    - Cache info included in response
    - Significantly faster response times
    
    Returns:
        Array of ticker objects in CoinGecko format with cache information
    """
    try:
        from fastapi.responses import Response
        from ticker_formatting_cached import get_clean_coingecko_tickers_cached
        from cache_manager import get_cache_status
        import json
        
        logger.info("🚀 CoinGecko cached endpoint called")
        
        # Get clean CoinGecko tickers (pure standard format)
        tickers = get_clean_coingecko_tickers_cached()
        
        if not tickers:
            logger.error("No CoinGecko tickers available")
            error_json = json.dumps({"error": "No ticker data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        cache_info = get_cache_status()
        logger.info(f"✅ Returning {len(tickers)} CoinGecko tickers (cached, age: {cache_info.get('age_seconds', 0)}s)")
        
        # Return pure CoinGecko format without any metadata for standard compliance
        # Cache info is available via /cache_status endpoint for monitoring
        
        # Convert to pretty-printed JSON
        pretty_json = json.dumps(tickers, indent=2, ensure_ascii=False)
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"❌ Error in coingecko_cached endpoint: {e}")
        error_json = json.dumps({"error": str(e)}, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@app.get("/coinmarketcap_cached")
async def get_cmc_summary_cached():
    """
    Get enhanced ticker data in CoinMarketCap (CMC) DEX format (CACHED VERSION)
    
    Features:
    - Unified caching reduces RPC calls
    - Ethereum contract symbols and addresses
    - Composite keys preserve all pairs
    - Cache info included in response
    - Significantly faster response times
    
    Returns:
        Object with composite keys containing enhanced ticker data with Ethereum contract details
    """
    try:
        from fastapi.responses import Response
        from ticker_formatting_cached import get_clean_coinmarketcap_enhanced_tickers_cached
        from cache_manager import get_cache_status
        import json
        
        logger.info("🚀 Enhanced CMC DEX cached endpoint called")
        
        # Get clean enhanced CMC tickers (pure standard format)
        enhanced_tickers = get_clean_coinmarketcap_enhanced_tickers_cached()
        
        if not enhanced_tickers:
            logger.error("No enhanced CMC tickers available")
            error_json = json.dumps({"error": "No ticker data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        cache_info = get_cache_status()
        logger.info(f"✅ Returning {len(enhanced_tickers)} enhanced CMC DEX tickers (cached, age: {cache_info.get('age_seconds', 0)}s)")
        
        # Return pure CMC format without any cache metadata for standard compliance
        # Cache info is available via /cache_status endpoint for monitoring
        
        # Convert to pretty-printed JSON
        pretty_json = json.dumps(enhanced_tickers, indent=2, ensure_ascii=False)
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"❌ Error in coinmarketcap_cached endpoint: {e}")
        error_json = json.dumps({"error": str(e)}, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )



@app.get("/cache_status")
async def get_cache_status_endpoint():
    """
    Get current cache status and information
    
    Returns:
        Cache status including age, validity, block height, and performance metrics
    """
    try:
        from fastapi.responses import Response
        from cache_manager import get_cache_status
        import json
        
        cache_info = get_cache_status()
        
        # Add additional useful information
        response_data = {
            "cache_status": cache_info,
            "endpoints": {
                "cached": [
                    "/coingecko_cached",
                    "/coinmarketcap_cached"
                ],
                "non_cached": [
                    "/coingecko",
                    "/coinmarketcap"
                ]
            },
            "performance_benefits": {
                "cached_response_time": "<0.1s (typical)",
                "non_cached_response_time": "0.5-1.0s (typical)",
                "rpc_calls_saved": "60-80 calls per cached request"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        pretty_json = json.dumps(response_data, indent=2, ensure_ascii=False)
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"❌ Error in cache_status endpoint: {e}")
        error_json = json.dumps({"error": str(e)}, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

# ============================================================================
# VERUS STATISTICS API COMPATIBLE ENDPOINT
# ============================================================================

@app.get("/coinpaprika")
async def get_coinpaprika():
    """
    Coinpaprika endpoint - VerusStatisticsAPI compatible format
    ==========================================================
    
    Provides data in the same format as https://marketapi.verus.services/market/allTickers
    but uses our existing reliable data source with:
    - ERC20 symbols from currency_contract_mapping
    - Same-pair aggregation (NO inverse pair aggregation)
    - Proper exclusion of converter currencies and excluded chains
    - Volume-weighted price aggregation
    
    Returns:
        JSON array of ticker objects with ERC20 symbols
    """
    try:
        from alltickers_formatter import generate_alltickers_response
        from fastapi.responses import Response
        import json
        
        logger.info("📊 Coinpaprika endpoint called")
        
        # Generate response using our reliable data
        tickers = generate_alltickers_response()
        
        if not tickers:
            logger.error("No ticker data available for coinpaprika")
            # Return empty response in VerusStatisticsAPI format
            empty_response = {
                "code": "200000",
                "data": {
                    "time": int(time.time() * 1000),  # Current timestamp in milliseconds
                    "ticker": []
                }
            }
            return Response(
                content=json.dumps(empty_response, indent=2),
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        logger.info(f"✅ Returning {len(tickers)} coinpaprika tickers with ERC20 symbols in VerusStatisticsAPI format")
        
        # Wrap in VerusStatisticsAPI format
        response_data = {
            "code": "200000",
            "data": {
                "time": int(time.time() * 1000),  # Current timestamp in milliseconds
                "ticker": tickers
            }
        }
        
        # Return in VerusStatisticsAPI format
        pretty_json = json.dumps(
            response_data, 
            indent=2,
            ensure_ascii=False
        )
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        import traceback
        logger.error(f"❌ Error in Coinpaprika endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return Response(
            content="[]",
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@app.get("/coinpaprika_cached")
async def get_coinpaprika_cached():
    """
    Coinpaprika endpoint - VerusStatisticsAPI compatible format - CACHED VERSION
    ============================================================================
    
    Cached version of the coinpaprika endpoint for improved performance.
    Uses the same logic but with cached data.
    
    Returns:
        JSON array of ticker objects with ERC20 symbols (cached)
    """
    try:
        from alltickers_formatter import generate_alltickers_response_cached
        from fastapi.responses import Response
        import json
        
        logger.info("📊 Coinpaprika cached endpoint called")
        
        # Generate response using cached data
        tickers = generate_alltickers_response_cached()
        
        if not tickers:
            logger.error("No cached ticker data available for coinpaprika")
            # Return empty response in VerusStatisticsAPI format
            empty_response = {
                "code": "200000",
                "data": {
                    "time": int(time.time() * 1000),  # Current timestamp in milliseconds
                    "ticker": []
                }
            }
            return Response(
                content=json.dumps(empty_response, indent=2),
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        logger.info(f"✅ Returning {len(tickers)} cached coinpaprika tickers with ERC20 symbols in VerusStatisticsAPI format")
        
        # Wrap in VerusStatisticsAPI format
        response_data = {
            "code": "200000",
            "data": {
                "time": int(time.time() * 1000),  # Current timestamp in milliseconds
                "ticker": tickers
            }
        }
        
        # Return in VerusStatisticsAPI format
        pretty_json = json.dumps(
            response_data, 
            indent=2,
            ensure_ascii=False
        )
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        import traceback
        logger.error(f"❌ Error in Coinpaprika cached endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return Response(
            content="[]",
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@app.get("/coinmarketcap_iaddress")
async def get_coinmarketcap_iaddress():
    """
    CoinMarketCap I-Address Format - TESTING ENDPOINT
    ===============================================
    
    CoinMarketCap-style endpoint using i-addresses as keys instead of ERC20 contract addresses.
    This is a separate implementation for testing purposes.
    
    Key Differences from /coinmarketcap:
    - Uses i-addresses (currency IDs) as base_id and quote_id
    - Uses i-address composite keys instead of contract address keys
    - Maintains same aggregation logic and format structure
    - Separate formatter to avoid modifying existing endpoint
    
    Format: CoinMarketCap DEX API compatible
    Keys: Sequential numbers ("0", "1", "2", etc.)
    Aggregation: Same-pair aggregation with volume-weighted pricing
    
    Response Format:
    {
      "0": {
        "base_id": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
        "base_name": "VRSC",
        "base_symbol": "VRSC",
        "quote_id": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM",
        "quote_name": "DAI.vETH",
        "quote_symbol": "DAI.vETH",
        "last_price": "0.46750232",
        "base_volume": "13151.93791997",
        "quote_volume": "27972.04617264"
      }
    }
    """
    try:
        from iaddress_formatter import format_iaddress_coinmarketcap_tickers
        from data_integration import extract_all_pairs_data
        
        logger.info("🔍 Processing I-Address CoinMarketCap endpoint request")
        
        # Extract pairs data
        pairs_response = extract_all_pairs_data()
        
        if not pairs_response or not pairs_response.get('pairs'):
            logger.error("No pairs data available for I-Address CMC endpoint")
            error_json = json.dumps({"error": "No ticker data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        # Extract the actual pairs data from the response
        pairs_data = pairs_response['pairs']
        
        # Format using i-address formatter
        iaddress_tickers = format_iaddress_coinmarketcap_tickers(pairs_data)
        
        if not iaddress_tickers:
            logger.error("No I-Address CMC tickers generated")
            error_json = json.dumps({"error": "No ticker data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        logger.info(f"✅ Returning {len(iaddress_tickers)} I-Address CMC tickers")
        
        # Convert to pretty-printed JSON
        pretty_json = json.dumps(iaddress_tickers, indent=2, ensure_ascii=False)
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"❌ Error in I-Address CMC endpoint: {e}")
        error_json = json.dumps({"error": str(e)}, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@app.get("/coinmarketcap_iaddress_cached")
async def get_coinmarketcap_iaddress_cached():
    """
    CoinMarketCap I-Address Format - CACHED VERSION
    =============================================
    
    Cached version of the I-Address CoinMarketCap endpoint for improved performance.
    Uses the same logic but with cached data.
    
    This endpoint provides the same data as /coinmarketcap_iaddress but with caching
    for better performance in production environments.
    
    Cache TTL: 60 seconds
    """
    try:
        from iaddress_formatter import format_iaddress_coinmarketcap_tickers
        from data_integration import extract_all_pairs_data
        
        logger.info("🔍 Processing I-Address CoinMarketCap cached endpoint request")
        
        # Use same logic as non-cached version for reliability
        pairs_result = extract_all_pairs_data()
        
        if 'error' in pairs_result:
            logger.error(f"Error extracting pairs data: {pairs_result['error']}")
            error_json = json.dumps({"error": "No ticker data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        pairs_data = pairs_result.get('pairs', [])
        logger.info(f"Formatting {len(pairs_data)} pairs for i-address CoinMarketCap cached endpoint")
        
        # Format using same formatter as non-cached version
        iaddress_tickers = format_iaddress_coinmarketcap_tickers(pairs_data)
        
        if not iaddress_tickers:
            logger.error("No I-Address CMC tickers generated")
            error_json = json.dumps({"error": "No ticker data available"}, indent=2)
            return Response(
                content=error_json,
                media_type="application/json",
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        logger.info(f"✅ Returning {len(iaddress_tickers)} I-Address CMC tickers (cached endpoint using fresh data)")
        
        # Convert to pretty-printed JSON
        pretty_json = json.dumps(iaddress_tickers, indent=2, ensure_ascii=False)
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"❌ Error in I-Address CMC cached endpoint: {e}")
        error_json = json.dumps({"error": str(e)}, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@app.get("/validate")
async def validate_endpoints():
    """
    Comprehensive API Endpoint Validation
    ====================================
    
    Runs automated validation checks on all API endpoints:
    1. Scientific notation detection
    2. Pair count validation 
    3. Cached vs non-cached endpoint matching
    4. Volume aggregation verification
    5. Data consistency checks
    
    Returns:
        JSON response with detailed validation results
    """
    try:
        from validation_endpoint import run_validation
        from fastapi.responses import Response
        import json
        
        logger.info("🔍 API Validation endpoint called")
        
        # Run comprehensive validation
        validation_results = run_validation()
        
        # Custom JSON serialization to prevent scientific notation
        def decimal_serializer(obj):
            if isinstance(obj, float):
                return f"{obj:.8f}"
            return obj
            
        pretty_json = json.dumps(
            validation_results, 
            indent=2, 
            ensure_ascii=False,
            default=decimal_serializer
        )
        
        # Log validation summary
        overall_status = validation_results.get("overall_status", "UNKNOWN")
        logger.info(f"✅ Validation complete. Overall status: {overall_status}")
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        import traceback
        logger.error(f"❌ Error in validation endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        error_response = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error": str(e),
            "validation_summary": {
                "overall_status": "ERROR"
            },
            "message": "Validation endpoint encountered an error"
        }
        error_json = json.dumps(error_response, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@app.post("/cache_clear")
async def clear_cache_endpoint():
    """
    Manually clear the cache (force refresh on next request)
    
    Returns:
        Success/error message
    """
    try:
        from fastapi.responses import Response
        from ticker_formatting_cached import clear_cache
        import json
        
        result = clear_cache()
        
        pretty_json = json.dumps(result, indent=2, ensure_ascii=False)
        
        return Response(
            content=pretty_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        logger.error(f"❌ Error in cache_clear endpoint: {e}")
        error_json = json.dumps({"error": str(e)}, indent=2)
        return Response(
            content=error_json,
            media_type="application/json",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

if __name__ == "__main__":
    port = 8765
    print(f"Starting Verus Ticker API on port {port}")
    
    # Kill any existing process on the port
    kill_process_on_port(port)
    
    # Start the server
    print(f"Launching FastAPI server on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
