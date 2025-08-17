# Verus API v1

A RESTful API service for accessing Verus blockchain data with multiple ticker format endpoints compatible with popular cryptocurrency data providers.

## 🚀 Quick Start

### Prerequisites

- Verus daemon running with RPC enabled
- Access to Verus daemon RPC credentials

### Configuration

Create a `.env` file in the project root with your Verus daemon configuration:

```env
# Verus Daemon RPC Configuration
# IMPORTANT: Replace these values with your actual Verus daemon credentials
# These must match the settings in your verus.conf file

# Standard RPC Connection Settings (VERUS_RPC_* format only)
VERUS_RPC_HOST=127.0.0.1
VERUS_RPC_PORT=27486
VERUS_RPC_URL=http://127.0.0.1:27486/
VERUS_RPC_USER=your_rpc_username
VERUS_RPC_PASSWORD=your_rpc_password
```

> **⚠️ Security Note**: Never commit your `.env` file to version control. Add it to your `.gitignore` file.

## 📚 API Endpoints

### 🏥 Health & Status

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Server status and RPC connection health |
| `GET /cache_status` | Cache information and current block height |
| `GET /validate` | Endpoint validation and connectivity test |

### 📊 Ticker Data

| Endpoint | Description | Format |
|----------|-------------|---------|
| `GET /coingecko` | CoinGecko compatible format | Array with pool_id |
| `GET /coinmarketcap` | CoinMarketCap compatible format | Object with composite keys |
| `GET /coinpaprika` | Coinpaprika compatible format | VerusStatisticsAPI compatible |
| `GET /coinmarketcap_iaddress` | CMC I-Address format | Testing with Verus native IDs |

### ⚡ Cached Endpoints

All cached endpoints have a **60-second TTL** for improved performance:

| Endpoint | Description |
|----------|-------------|
| `GET /coingecko_cached` | CoinGecko format (cached) |
| `GET /coinmarketcap_cached` | CoinMarketCap format (cached) |
| `GET /coinpaprika_cached` | Coinpaprika format (cached) |
| `GET /coinmarketcap_iaddress_cached` | CMC I-Address format (cached) |

## 📝 Response Formats

### CoinGecko Format
Returns an array with pool_id for compatibility with CoinGecko API structure.

### CoinMarketCap Format
Returns an object with composite keys following CoinMarketCap API conventions.

### Coinpaprika Format
Compatible with VerusStatisticsAPI, following Coinpaprika's data structure.

### CMC I-Address Format
Experimental Coinmarketcap I-Address format for testing with Verus native identity addresses.

## 📊 Caching

The API implements intelligent caching with a 60-second TTL to balance data freshness with performance. Cached endpoints are available for all ticker data formats.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Version**: 1.0.0  
**Status**: Active Development  
**Compatibility**: Verus Protocol
