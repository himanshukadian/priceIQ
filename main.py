#!/usr/bin/env python3
"""
Price Intelligence Platform - Main CLI Entry Point
"""
import json
import sys
import os
from typing import Optional

CONFIG_PATH = os.path.join("config", "phase1_config.yaml")

# Try to import Typer, fallback to argparse if not available
try:
    import typer
    USE_TYPER = True
except ImportError:
    import argparse
    USE_TYPER = False

from src.orchestrator.interface import Orchestrator

def run_pipeline(user_input):
    """
    Run the orchestrator pipeline and print results as pretty JSON.
    """
    orchestrator = Orchestrator(CONFIG_PATH)
    results = orchestrator.run(user_input)
    print(json.dumps(results, indent=2, ensure_ascii=False))

if USE_TYPER:
    app = typer.Typer(help="Price Intelligence CLI - Run the full mock pipeline.")

    @app.command()
    def main(
        query: str = typer.Option(None, help="Product search query, e.g. 'iPhone 16 Pro, 128GB'"),
        country: str = typer.Option(None, help="Country code, e.g. 'US'"),
        input_file: str = typer.Option(None, help="Path to JSON file with input (keys: 'query', 'country')")
    ):
        """
        Run the price intelligence pipeline with CLI or file input.
        """
        if input_file:
            if not os.path.exists(input_file):
                typer.echo(f"❌ Input file not found: {input_file}", err=True)
                raise typer.Exit(1)
            with open(input_file, 'r', encoding='utf-8') as f:
                try:
                    user_input = json.load(f)
                except Exception as e:
                    typer.echo(f"❌ Failed to parse input file: {e}", err=True)
                    raise typer.Exit(1)
        else:
            if not query or not country:
                typer.echo("❌ Must provide both --query and --country, or --input_file", err=True)
                raise typer.Exit(1)
            user_input = {"query": query, "country": country}
        run_pipeline(user_input)

    if __name__ == "__main__":
        app()
else:
    def main():
        """
        Fallback CLI using argparse if Typer is not available.
        """
        import argparse
        parser = argparse.ArgumentParser(description="Price Intelligence CLI - Run the full mock pipeline.")
        parser.add_argument('--query', type=str, help="Product search query, e.g. 'iPhone 16 Pro, 128GB'")
        parser.add_argument('--country', type=str, help="Country code, e.g. 'US'")
        parser.add_argument('--input_file', type=str, help="Path to JSON file with input (keys: 'query', 'country')")
        args = parser.parse_args()

        if args.input_file:
            if not os.path.exists(args.input_file):
                print(f"❌ Input file not found: {args.input_file}", file=sys.stderr)
                sys.exit(1)
            with open(args.input_file, 'r', encoding='utf-8') as f:
                try:
                    user_input = json.load(f)
                except Exception as e:
                    print(f"❌ Failed to parse input file: {e}", file=sys.stderr)
                    sys.exit(1)
        else:
            if not args.query or not args.country:
                print("❌ Must provide both --query and --country, or --input_file", file=sys.stderr)
                sys.exit(1)
            user_input = {"query": args.query, "country": args.country}
        run_pipeline(user_input)

    if __name__ == "__main__":
        main() 