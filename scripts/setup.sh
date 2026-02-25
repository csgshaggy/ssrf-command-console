#!/usr/bin/env bash

set -e

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
BLUE="\033[1;34m"
NC="\033[0m"

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}        SSRF Command Console — Environment Setup            ${NC}"
echo -e "${BLUE}============================================================${NC}"

# ------------------------------------------------------------
# 1. Verify project root
# ------------------------------------------------------------
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}ERROR:${NC} requirements.txt not found. Run this script from project root."
    exit 1
fi

echo -e "${GREEN}✔ Project root verified${NC}"

# ------------------------------------------------------------
# 2. Create virtual environment if missing
# ------------------------------------------------------------
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✔ Virtual environment created${NC}"
else
    echo -e "${GREEN}✔ Virtual environment already exists${NC}"
fi

# ------------------------------------------------------------
# 3. Activate venv
# ------------------------------------------------------------
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✔ venv activated${NC}"

# ------------------------------------------------------------
# 4. Install dependencies
# ------------------------------------------------------------
echo -e "${YELLOW}Installing pinned dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✔ Dependencies installed${NC}"

# ------------------------------------------------------------
# 5. Verify .env presence
# ------------------------------------------------------------
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}WARNING:${NC} .env file not found."
    echo -e "Create one with your Google OAuth + JWT secrets:"
    echo -e "  GOOGLE_CLIENT_ID=..."
    echo -e "  GOOGLE_CLIENT_SECRET=..."
    echo -e "  JWT_SECRET=..."
else
    echo -e "${GREEN}✔ .env file detected${NC}"
fi

# ------------------------------------------------------------
# 6. Structure check
# ------------------------------------------------------------
echo -e "${YELLOW}Verifying project structure...${NC}"

declare -a paths=(
    "app"
    "app/main.py"
    "app/auth.py"
    "app/config.py"
    "dispatcher.py"
    "dashboard_web.py"
    "modes"
    "console"
    "requirements.txt"
)

for p in "${paths[@]}"; do
    if [ -e "$p" ]; then
        echo -e "${GREEN}✔ $p${NC}"
    else
        echo -e "${RED}✘ Missing: $p${NC}"
    fi
done

# ------------------------------------------------------------
# 7. Backend health check
# ------------------------------------------------------------
echo -e "${YELLOW}Testing backend import...${NC}"

python3 - << 'EOF'
try:
    import app.main
    print("✔ Backend import OK")
except Exception as e:
    print("✘ Backend import FAILED:", e)
    exit(1)
EOF

# ------------------------------------------------------------
# 8. Final summary
# ------------------------------------------------------------
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}Environment setup complete.${NC}"
echo -e ""
echo -e "Start backend:"
echo -e "  ${YELLOW}uvicorn app.main:app --reload${NC}"
echo -e ""
echo -e "Start dashboard:"
echo -e "  ${YELLOW}uvicorn dashboard_web:app --reload${NC}"
echo -e ""
echo -e "${BLUE}============================================================${NC}"
