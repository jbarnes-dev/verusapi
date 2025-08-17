This is v1 of the new verus API.

Make sure you create a .env file in the following format.

# Verus Daemon RPC Configuration
# IMPORTANT: Replace these values with your actual Verus daemon credentials
# These must match the settings in your verus.conf file

# Standard RPC Connection Settings (VERUS_RPC_* format only)
VERUS_RPC_HOST=127.0.0.1
VERUS_RPC_PORT=27486
VERUS_RPC_URL=http://127.0.0.1:27486/
VERUS_RPC_USER=
VERUS_RPC_PASSWORD=



📡 API Endpoints
🏥 Health & Status
GET /health - Server status and RPC connection
GET /cache_status - Cache information and block height
GET /validate - Endpoint validation
📊 Ticker Data
GET /coingecko - CoinGecko format (array with pool_id)
GET /coinmarketcap - CoinMarketCap format (object with composite keys)
GET /coinpaprika - Coinpaprika format (VerusStatisticsAPI compatible)
GET /coinmarketcap_iaddress - CMC I-Address format (testing with Verus native IDs)
⚡ Cached Endpoints (60s TTL)
GET /coingecko_cached - CoinGecko cached
GET /coinmarketcap_cached - CoinMarketCap cached
GET /coinpaprika_cached - Coinpaprika cached
GET /coinmarketcap_iaddress_cached - CMC I-Address cached
