#!/usr/bin/env python3
"""Solana AI Agent — Main Entry Point"""
import argparse
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from core.monitor import TokenMonitor
from core.analytics import DeFiAnalytics
from core.signals import SignalGenerator


async def main():
    parser = argparse.ArgumentParser(description="Solana AI Agent")
    parser.add_argument("--mode", choices=["monitor", "analytics", "signals"], default="monitor")
    parser.add_argument("--token", help="Token mint address to track")
    parser.add_argument("--wallet", help="Wallet address to monitor")
    args = parser.parse_args()

    rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

    if args.mode == "monitor":
        monitor = TokenMonitor(rpc_url)
        await monitor.start(token_mint=args.token)
    elif args.mode == "analytics":
        analytics = DeFiAnalytics(rpc_url)
        report = await analytics.generate_report()
        print(report)
    elif args.mode == "signals":
        signals = SignalGenerator(rpc_url)
        await signals.run()


if __name__ == "__main__":
    asyncio.run(main())
