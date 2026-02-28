"""DeFi analytics for Solana ecosystem."""
import httpx


class DeFiAnalytics:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url

    async def get_top_tokens(self, limit: int = 10) -> list:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://token.jup.ag/strict")
            tokens = r.json()[:limit]
            return [{"symbol": t["symbol"], "name": t["name"], "address": t["address"]} for t in tokens]

    async def generate_report(self) -> str:
        tokens = await self.get_top_tokens()
        lines = ["# Solana DeFi Report\n"]
        for t in tokens:
            lines.append(f"- **{t['symbol']}** ({t['name']}): `{t['address'][:12]}...`")
        return "\n".join(lines)
