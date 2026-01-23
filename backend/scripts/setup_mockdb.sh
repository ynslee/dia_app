#!/usr/bin/env bash
set -euo pipefail

# --- CONFIG ---
ENV_NAME="diabetes-api"
DB_URL="mysql+asyncmy://diabetes:diabetes@localhost:3307/diabetes_mock"

echo "👉 Setting up mock environment using Conda env '$ENV_NAME' and MySQL at $DB_URL"

# 1) Load conda into this shell
if command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
else
  echo "❌ Conda not found. Please install Miniconda/Anaconda first."
  exit 1
fi

# 2) Recreate env every time (delete if exists)
if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  echo "🧹 Removing existing conda env '$ENV_NAME'..."
  conda env remove -n "$ENV_NAME" -y
fi

echo "🔧 Creating conda env '$ENV_NAME' from environment.yml..."
conda env create -f environment.yml


# 3) Activate the env
echo "🔁 Activating env '$ENV_NAME'..."
conda activate "$ENV_NAME"

# 4) Start MySQL mock DB via docker compose
echo "🐳 Starting MySQL mock DB with docker compose..."
docker compose up -d mysql-mock

# 5) Export DATABASE_URL for Python scripts
export DATABASE_URL="$DB_URL"

# 6) Initialize schema and seed data
echo "📦 Initializing database schema..."
python init_mock_db.py

echo "🌱 Seeding mock data..."
python seed_mock_db.py

echo "✅ All done! Mock DB is ready."
echo "   DATABASE_URL=$DATABASE_URL"

#echo "🚀 Starting API server..."
#python -m uvicorn main:app --reload