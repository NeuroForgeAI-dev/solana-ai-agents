"""Real-time Solana token monitoring."""
import asyncio
import httpx
from datetime import datetime


class TokenMonitor:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url

    async def get_token_info(self, mint: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.rpc_url, json={
                "jsonrpc": "2.0", "id": 1,
                "method": "getAccountInfo",
                "params": [mint, {"encoding": "jsonParsed"}],
            })
            return response.json().get("result", {})

    async def get_price(self, mint: str) -> float:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://price.jup.ag/v6/price?ids={mint}")
            data = r.json().get("data", {}).get(mint, {})
            return data.get("price", 0.0)

    async def start(self, token_mint: str = None, interval: int = 10):
        mint = token_mint or "So11111111111111111111111111111111111111112"  # SOL
        print(f"[{datetime.now()}] Monitoring {mint}...")

        while True:
            price = await self.get_price(mint)
            print(f"[{datetime.now()}] Price: ${price:.4f}")
            await asyncio.sleep(interval)
