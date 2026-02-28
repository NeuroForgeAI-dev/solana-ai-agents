"""AI-powered trading signal generator."""
import asyncio
from core.monitor import TokenMonitor


class SignalGenerator:
    def __init__(self, rpc_url: str):
        self.monitor = TokenMonitor(rpc_url)
        self.price_history = []

    def analyze(self, prices: list) -> str:
        if len(prices) < 3:
            return "HOLD"
        avg = sum(prices) / len(prices)
        current = prices[-1]
        if current > avg * 1.05:
            return "SELL"
        elif current < avg * 0.95:
            return "BUY"
        return "HOLD"

    async def run(self, mint: str = None, interval: int = 30):
        mint = mint or "So11111111111111111111111111111111111111112"
        print(f"Signal generator started for {mint}")

        while True:
            price = await self.monitor.get_price(mint)
            self.price_history.append(price)
            if len(self.price_history) > 20:
                self.price_history = self.price_history[-20:]

            signal = self.analyze(self.price_history)
            print(f"Price: ${price:.4f} | Signal: {signal}")
            await asyncio.sleep(interval)
