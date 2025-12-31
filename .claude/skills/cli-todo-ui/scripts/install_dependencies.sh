#!/bin/bash
# Install dependencies for CLI Todo UI applications

set -e

echo "Installing CLI Todo UI dependencies..."

# Core dependencies
pip install "textual>=0.63.0" "rich>=13.7.0"

# Optional enhancements
echo "Installing optional dependencies..."
pip install "pydantic>=2.0.0" "python-dateutil>=2.8.0"

echo "✓ Dependencies installed successfully!"
echo ""
echo "Quick start:"
echo "  python -m textual --version  # Verify Textual installation"
echo "  textual --help              # View Textual CLI options"
