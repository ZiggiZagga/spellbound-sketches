import logging
import os
import json
import typer

# Configure logging
logging.basicConfig(level=logging.INFO)
name = "Spellbound Sketch CLI"
logger = logging.getLogger(name)

app = typer.Typer(pretty_exceptions_enable=False)

@app.command()
def run_sketch():
    logger.info(f"run-sketch")


if __name__ == "__main__":
    app()
