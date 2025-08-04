#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Smart Contact Router Application${NC}"

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    exit 0
}

# Set up trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start backend server
echo -e "${GREEN}📡 Starting FastAPI backend server on port 8001...${NC}"
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || echo "Virtual environment not found, using global Python"
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo -e "${GREEN}🌐 Starting React frontend server on port 3000...${NC}"
cd frontend

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    npm install
fi

npm start &
FRONTEND_PID=$!

echo -e "${BLUE}✅ Both servers are starting up!${NC}"
echo -e "${GREEN}🔗 Frontend: http://localhost:3000${NC}"
echo -e "${GREEN}🔗 Backend API: http://localhost:8001${NC}"
echo -e "${GREEN}🔗 API Health Check: http://localhost:8001/health${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Wait for either process to exit
wait
