"""
FastAPI backend for Debt Analysis Tool
RESTful API endpoints for debt analysis and roadmap generation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import logging
from debt_analyzer import process_debt_analysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Debt Freedom Analyzer API",
    description="API for analyzing debt and generating repayment roadmaps",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class DebtInput(BaseModel):
    """Single debt input model"""
    name: str = Field(..., description="Name of the debt (e.g., 'Visa Credit Card')")
    balance: float = Field(..., gt=0, description="Current balance in dollars")
    interest_rate: float = Field(..., ge=0, le=100, description="Annual interest rate as percentage")
    minimum_payment: float = Field(..., gt=0, description="Minimum monthly payment in dollars")
    debt_type: Optional[str] = Field("other", description="Type of debt: credit_card, personal_loan, auto_loan, student_loan, mortgage, medical, other")
    
    @validator('balance', 'minimum_payment')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return round(v, 2)
    
    @validator('interest_rate')
    def validate_interest_rate(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Interest rate must be between 0 and 100')
        return round(v, 2)


class AnalysisRequest(BaseModel):
    """Complete analysis request model"""
    debts: List[DebtInput] = Field(..., min_items=1, description="List of debts to analyze")
    monthly_budget: float = Field(..., gt=0, description="Monthly budget available for debt payments")
    
    @validator('monthly_budget')
    def validate_budget(cls, v):
        if v <= 0:
            raise ValueError('Monthly budget must be positive')
        return round(v, 2)
    
    @validator('debts')
    def validate_debts(cls, v):
        if not v:
            raise ValueError('At least one debt is required')
        if len(v) > 50:
            raise ValueError('Maximum 50 debts allowed')
        return v


class AnalysisResponse(BaseModel):
    """Analysis response model"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "status": "healthy",
        "message": "Debt Freedom Analyzer API",
        "version": "1.0.0",
        "description": "Helps you escape debt traps with intelligent analysis and repayment roadmaps",
        "endpoints": {
            "/health": "Health check",
            "/api/analyze": "POST - Analyze debts and get repayment roadmap",
            "/api/calculate": "POST - Calculate specific repayment strategy",
            "/docs": "Interactive API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "debt-analyzer",
        "timestamp": str(__import__('datetime').datetime.now())
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_debts(request: AnalysisRequest):
    """
    Main endpoint: Analyze debts and generate comprehensive repayment roadmap
    
    This endpoint:
    - Analyzes your debt situation
    - Identifies problem areas
    - Calculates 3 repayment strategies (Avalanche, Snowball, Hybrid)
    - Recommends the best strategy for your situation
    - Provides actionable steps and milestones
    """
    try:
        logger.info(f"Received analysis request for {len(request.debts)} debts")
        
        # Validate that budget covers minimum payments
        total_minimum = sum(debt.minimum_payment for debt in request.debts)
        if request.monthly_budget < total_minimum:
            raise HTTPException(
                status_code=400,
                detail=f"Monthly budget (${request.monthly_budget:.2f}) is less than total minimum payments (${total_minimum:.2f}). You need at least ${total_minimum:.2f} per month."
            )
        
        # Convert to dict format for processor
        debt_data = [debt.dict() for debt in request.debts]
        
        # Process analysis
        result = process_debt_analysis(debt_data, request.monthly_budget)
        
        logger.info("Analysis completed successfully")
        
        return AnalysisResponse(
            success=True,
            data=result
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again."
        )


@app.post("/api/calculate")
async def calculate_strategy(request: AnalysisRequest, strategy: str = "avalanche"):
    """
    Calculate specific repayment strategy
    
    Strategies:
    - avalanche: Pay highest interest rate debts first (saves most money)
    - snowball: Pay smallest balance debts first (quick psychological wins)
    - hybrid: Combination approach
    """
    try:
        if strategy not in ["avalanche", "snowball", "hybrid"]:
            raise HTTPException(
                status_code=400,
                detail="Strategy must be one of: avalanche, snowball, hybrid"
            )
        
        debt_data = [debt.dict() for debt in request.debts]
        result = process_debt_analysis(debt_data, request.monthly_budget)
        
        # Return only the requested strategy
        strategy_data = result["repayment_strategies"].get(strategy)
        
        return {
            "success": True,
            "strategy": strategy,
            "data": strategy_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quick-analysis")
async def quick_analysis(request: AnalysisRequest):
    """
    Quick analysis endpoint - returns only summary without detailed roadmap
    Useful for initial assessment
    """
    try:
        debt_data = [debt.dict() for debt in request.debts]
        result = process_debt_analysis(debt_data, request.monthly_budget)
        
        # Return only analysis and problems, not full roadmap
        return {
            "success": True,
            "data": {
                "analysis": result["analysis"],
                "problems": result["problems"],
                "quick_comparison": result["comparison"]
            }
        }
    
    except Exception as e:
        logger.error(f"Error in quick analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/debt-types")
async def get_debt_types():
    """Get list of supported debt types"""
    return {
        "debt_types": [
            {"value": "credit_card", "label": "Credit Card"},
            {"value": "personal_loan", "label": "Personal Loan"},
            {"value": "auto_loan", "label": "Auto Loan"},
            {"value": "student_loan", "label": "Student Loan"},
            {"value": "mortgage", "label": "Mortgage"},
            {"value": "medical", "label": "Medical Debt"},
            {"value": "other", "label": "Other"}
        ]
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
