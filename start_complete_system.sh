#!/bin/bash

# Complete Resume Optimizer System Startup Script
# Starts both backend API and frontend web application

echo "🚀 Starting Complete Resume Optimizer System..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}Waiting for $service_name to be ready...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "\n${RED}❌ $service_name failed to start after $max_attempts attempts${NC}"
    return 1
}

# Check if backend is already running
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Backend API is already running on port 8000${NC}"
else
    echo -e "${BLUE}🔧 Starting Backend API...${NC}"
    cd /workspace
    python3 main.py &
    BACKEND_PID=$!
    
    # Wait for backend to be ready
    if wait_for_service "http://localhost:8000/health" "Backend API"; then
        echo -e "${GREEN}✅ Backend API started successfully (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${RED}❌ Failed to start Backend API${NC}"
        exit 1
    fi
fi

# Check if frontend is already running
if check_port 3000; then
    echo -e "${YELLOW}⚠️  Frontend server is already running on port 3000${NC}"
else
    echo -e "${BLUE}🌐 Starting Frontend Server...${NC}"
    cd /workspace/frontend
    python3 server.py &
    FRONTEND_PID=$!
    
    # Wait for frontend to be ready
    if wait_for_service "http://localhost:3000" "Frontend Server"; then
        echo -e "${GREEN}✅ Frontend Server started successfully (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${RED}❌ Failed to start Frontend Server${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}🎉 Complete Resume Optimizer System is Running!${NC}"
echo "=============================================="
echo -e "${BLUE}📊 Backend API:${NC} http://localhost:8000"
echo -e "${BLUE}📊 API Docs:${NC} http://localhost:8000/docs"
echo -e "${BLUE}🌐 Frontend:${NC} http://localhost:3000"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "• Upload your resume in PDF, DOCX, or TXT format"
echo "• Provide a detailed job description for better optimization"
echo "• Use the side-by-side comparison to see improvements"
echo "• Download or copy your optimized resume"
echo ""
echo -e "${YELLOW}🛑 To stop the system:${NC}"
echo "• Press Ctrl+C to stop this script"
echo "• Or run: pkill -f 'python3 main.py' && pkill -f 'python3 server.py'"
echo ""

# Function to handle cleanup on script exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping Resume Optimizer System...${NC}"
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Backend API stopped${NC}"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Frontend Server stopped${NC}"
    fi
    
    echo -e "${GREEN}🎉 System stopped successfully${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running and show status
echo -e "${BLUE}📈 System Status:${NC}"
echo "• Backend API: Running on port 8000"
echo "• Frontend Server: Running on port 3000"
echo "• Ready to optimize resumes!"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the system${NC}"

# Keep the script running
while true; do
    sleep 10
    
    # Check if services are still running
    if ! check_port 8000; then
        echo -e "${RED}❌ Backend API stopped unexpectedly${NC}"
        break
    fi
    
    if ! check_port 3000; then
        echo -e "${RED}❌ Frontend Server stopped unexpectedly${NC}"
        break
    fi
done

cleanup