"""
Debt Analysis and Repayment Roadmap Tool
Backend Engine for Debt Analysis and Optimization
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class Debt:
    """Represents a single debt/loan"""
    name: str
    balance: float
    interest_rate: float  # Annual percentage rate
    minimum_payment: float
    debt_type: str  # credit_card, personal_loan, auto_loan, student_loan, etc.
    
    def monthly_interest_rate(self) -> float:
        """Calculate monthly interest rate"""
        return self.interest_rate / 100 / 12
    
    def calculate_interest(self) -> float:
        """Calculate monthly interest amount"""
        return self.balance * self.monthly_interest_rate()


class DebtAnalyzer:
    """Analyzes debt situation and provides insights"""
    
    def __init__(self, debts: List[Debt], monthly_budget: float):
        self.debts = debts
        self.monthly_budget = monthly_budget
        self.total_minimum_payment = sum(debt.minimum_payment for debt in debts)
        self.extra_payment = max(0, monthly_budget - self.total_minimum_payment)
    
    def get_total_debt(self) -> float:
        """Calculate total debt balance"""
        return sum(debt.balance for debt in self.debts)
    
    def get_weighted_interest_rate(self) -> float:
        """Calculate weighted average interest rate"""
        total_debt = self.get_total_debt()
        if total_debt == 0:
            return 0
        
        weighted_sum = sum(debt.balance * debt.interest_rate for debt in self.debts)
        return weighted_sum / total_debt
    
    def get_total_monthly_interest(self) -> float:
        """Calculate total monthly interest across all debts"""
        return sum(debt.calculate_interest() for debt in self.debts)
    
    def analyze_debt_situation(self) -> Dict[str, Any]:
        """Comprehensive debt situation analysis"""
        total_debt = self.get_total_debt()
        avg_interest_rate = self.get_weighted_interest_rate()
        monthly_interest = self.get_total_monthly_interest()
        
        # Debt-to-income considerations
        budget_utilization = (self.total_minimum_payment / self.monthly_budget * 100) if self.monthly_budget > 0 else 0
        
        # Find highest and lowest interest debts
        highest_interest_debt = max(self.debts, key=lambda d: d.interest_rate) if self.debts else None
        lowest_interest_debt = min(self.debts, key=lambda d: d.interest_rate) if self.debts else None
        
        # Categorize debt severity
        if budget_utilization > 50:
            severity = "Critical"
            severity_message = "Your minimum payments exceed 50% of your budget. Immediate action required!"
        elif budget_utilization > 35:
            severity = "High"
            severity_message = "Your debt load is high. Focus on aggressive repayment."
        elif budget_utilization > 20:
            severity = "Moderate"
            severity_message = "Your debt is manageable but needs attention."
        else:
            severity = "Low"
            severity_message = "Your debt situation is under control. Keep up the good work!"
        
        return {
            "total_debt": round(total_debt, 2),
            "number_of_debts": len(self.debts),
            "weighted_avg_interest_rate": round(avg_interest_rate, 2),
            "total_monthly_interest": round(monthly_interest, 2),
            "total_minimum_payment": round(self.total_minimum_payment, 2),
            "monthly_budget": round(self.monthly_budget, 2),
            "extra_payment_capacity": round(self.extra_payment, 2),
            "budget_utilization_percentage": round(budget_utilization, 2),
            "severity": severity,
            "severity_message": severity_message,
            "highest_interest_debt": {
                "name": highest_interest_debt.name,
                "rate": highest_interest_debt.interest_rate,
                "balance": highest_interest_debt.balance
            } if highest_interest_debt else None,
            "lowest_interest_debt": {
                "name": lowest_interest_debt.name,
                "rate": lowest_interest_debt.interest_rate,
                "balance": lowest_interest_debt.balance
            } if lowest_interest_debt else None,
            "yearly_interest_cost": round(monthly_interest * 12, 2)
        }
    
    def identify_problems(self) -> List[Dict[str, str]]:
        """Identify specific problems in debt management"""
        problems = []
        
        # High interest rate debts
        high_interest_debts = [d for d in self.debts if d.interest_rate > 18]
        if high_interest_debts:
            problems.append({
                "type": "High Interest Rates",
                "severity": "high",
                "description": f"You have {len(high_interest_debts)} debt(s) with interest rates above 18%. These are costing you significant money.",
                "recommendation": "Prioritize paying off high-interest debts first or consider balance transfer options."
            })
        
        # Minimum payment trap
        if self.extra_payment < self.total_minimum_payment * 0.2:
            problems.append({
                "type": "Minimum Payment Trap",
                "severity": "high",
                "description": "You're mostly paying minimum payments, which means you're paying mostly interest.",
                "recommendation": "Try to allocate at least 20% more than minimum payments to reduce principal faster."
            })
        
        # Budget overload
        budget_utilization = (self.total_minimum_payment / self.monthly_budget * 100) if self.monthly_budget > 0 else 0
        if budget_utilization > 50:
            problems.append({
                "type": "Budget Overload",
                "severity": "critical",
                "description": "More than 50% of your budget goes to minimum debt payments.",
                "recommendation": "Consider debt consolidation, seeking credit counseling, or finding ways to increase income."
            })
        
        # Multiple small debts
        small_debts = [d for d in self.debts if d.balance < 1000]
        if len(small_debts) >= 3:
            problems.append({
                "type": "Multiple Small Debts",
                "severity": "medium",
                "description": f"You have {len(small_debts)} small debts under $1,000 each.",
                "recommendation": "Consider using the Debt Snowball method to quickly eliminate these for psychological wins."
            })
        
        # High credit card utilization
        credit_cards = [d for d in self.debts if d.debt_type == "credit_card"]
        if credit_cards:
            problems.append({
                "type": "Credit Card Debt",
                "severity": "medium",
                "description": f"You have {len(credit_cards)} credit card debt(s) totaling ${sum(d.balance for d in credit_cards):,.2f}.",
                "recommendation": "Credit cards typically have the highest interest rates. Focus on these first."
            })
        
        return problems


class DebtPayoffCalculator:
    """Calculate debt payoff strategies"""
    
    @staticmethod
    def calculate_avalanche_method(debts: List[Debt], monthly_payment: float) -> Dict[str, Any]:
        """
        Avalanche Method: Pay off highest interest rate debts first
        Saves the most money but may take longer for first payoff
        """
        # Sort debts by interest rate (highest first)
        sorted_debts = sorted(debts, key=lambda d: d.interest_rate, reverse=True)
        return DebtPayoffCalculator._simulate_payoff(sorted_debts, monthly_payment, "Avalanche (Highest Interest First)")
    
    @staticmethod
    def calculate_snowball_method(debts: List[Debt], monthly_payment: float) -> Dict[str, Any]:
        """
        Snowball Method: Pay off smallest balance debts first
        Provides psychological wins with quick payoffs
        """
        # Sort debts by balance (smallest first)
        sorted_debts = sorted(debts, key=lambda d: d.balance)
        return DebtPayoffCalculator._simulate_payoff(sorted_debts, monthly_payment, "Snowball (Smallest Balance First)")
    
    @staticmethod
    def calculate_hybrid_method(debts: List[Debt], monthly_payment: float) -> Dict[str, Any]:
        """
        Hybrid Method: Prioritize high-interest debts with balance under $2000 first,
        then highest interest rates
        """
        # Separate into quick wins (high interest, low balance) and rest
        quick_wins = [d for d in debts if d.interest_rate > 15 and d.balance < 2000]
        remaining = [d for d in debts if d not in quick_wins]
        
        # Sort quick wins by balance, remaining by interest rate
        quick_wins_sorted = sorted(quick_wins, key=lambda d: d.balance)
        remaining_sorted = sorted(remaining, key=lambda d: d.interest_rate, reverse=True)
        
        sorted_debts = quick_wins_sorted + remaining_sorted
        return DebtPayoffCalculator._simulate_payoff(sorted_debts, monthly_payment, "Hybrid (Quick Wins + High Interest)")
    
    @staticmethod
    def _simulate_payoff(debts: List[Debt], monthly_payment: float, method_name: str) -> Dict[str, Any]:
        """Simulate debt payoff and calculate timeline"""
        import copy
        
        # Create copies to avoid modifying originals
        working_debts = [copy.deepcopy(debt) for debt in debts]
        
        total_paid = 0
        total_interest_paid = 0
        months = 0
        payoff_timeline = []
        monthly_breakdown = []
        
        max_months = 600  # 50 years max to prevent infinite loops
        
        while working_debts and months < max_months:
            months += 1
            remaining_payment = monthly_payment
            month_total_interest = 0
            month_total_principal = 0
            
            # Calculate interest for all debts
            for debt in working_debts:
                interest = debt.calculate_interest()
                month_total_interest += interest
                total_interest_paid += interest
            
            # Pay minimum on all debts
            for debt in working_debts:
                interest = debt.calculate_interest()
                principal = min(debt.minimum_payment - interest, debt.balance)
                
                debt.balance -= principal
                remaining_payment -= debt.minimum_payment
                month_total_principal += principal
                total_paid += debt.minimum_payment
            
            # Apply extra payment to first debt in priority order
            if remaining_payment > 0 and working_debts:
                target_debt = working_debts[0]
                extra_principal = min(remaining_payment, target_debt.balance)
                target_debt.balance -= extra_principal
                month_total_principal += extra_principal
                total_paid += extra_principal
            
            # Record monthly breakdown (only first 12 months to avoid huge data)
            if months <= 12:
                monthly_breakdown.append({
                    "month": months,
                    "total_payment": round(monthly_payment, 2),
                    "principal_paid": round(month_total_principal, 2),
                    "interest_paid": round(month_total_interest, 2),
                    "remaining_balance": round(sum(d.balance for d in working_debts), 2)
                })
            
            # Check for paid off debts
            paid_off = [debt for debt in working_debts if debt.balance <= 0.01]
            for debt in paid_off:
                payoff_timeline.append({
                    "debt_name": debt.name,
                    "month": months,
                    "years_months": f"{months // 12} years, {months % 12} months"
                })
                working_debts.remove(debt)
        
        total_cost = total_paid
        years = months // 12
        remaining_months = months % 12
        
        return {
            "method_name": method_name,
            "total_months": months,
            "years": years,
            "remaining_months": remaining_months,
            "time_to_debt_free": f"{years} years, {remaining_months} months",
            "total_amount_paid": round(total_cost, 2),
            "total_interest_paid": round(total_interest_paid, 2),
            "total_principal": round(sum(debt.balance for debt in debts), 2),
            "payoff_order": [debt.name for debt in debts],
            "payoff_timeline": payoff_timeline,
            "monthly_breakdown": monthly_breakdown,
            "average_monthly_payment": round(monthly_payment, 2)
        }


class RoadmapGenerator:
    """Generates actionable debt repayment roadmap"""
    
    def __init__(self, debts: List[Debt], monthly_budget: float):
        self.debts = debts
        self.monthly_budget = monthly_budget
        self.analyzer = DebtAnalyzer(debts, monthly_budget)
    
    def generate_roadmap(self) -> Dict[str, Any]:
        """Generate comprehensive debt repayment roadmap"""
        
        # Get analysis
        analysis = self.analyzer.analyze_debt_situation()
        problems = self.analyzer.identify_problems()
        
        # Calculate all three methods
        avalanche = DebtPayoffCalculator.calculate_avalanche_method(
            self.debts, self.monthly_budget
        )
        snowball = DebtPayoffCalculator.calculate_snowball_method(
            self.debts, self.monthly_budget
        )
        hybrid = DebtPayoffCalculator.calculate_hybrid_method(
            self.debts, self.monthly_budget
        )
        
        # Determine best method
        if analysis["severity"] in ["Critical", "High"]:
            recommended_method = avalanche
            recommendation_reason = "Avalanche method recommended to minimize interest costs in your high-debt situation."
        elif len(self.debts) >= 5:
            recommended_method = snowball
            recommendation_reason = "Snowball method recommended to build momentum with quick wins given your multiple debts."
        else:
            recommended_method = hybrid
            recommendation_reason = "Hybrid method recommended for balance between savings and psychological wins."
        
        # Generate action steps
        action_steps = self._generate_action_steps(analysis, problems, recommended_method)
        
        # Generate milestones
        milestones = self._generate_milestones(recommended_method)
        
        # Generate tips
        tips = self._generate_tips(analysis)
        
        return {
            "analysis": analysis,
            "problems": problems,
            "repayment_strategies": {
                "avalanche": avalanche,
                "snowball": snowball,
                "hybrid": hybrid
            },
            "recommended_strategy": {
                "method": recommended_method,
                "reason": recommendation_reason
            },
            "action_plan": action_steps,
            "milestones": milestones,
            "tips": tips,
            "comparison": {
                "time_saved_avalanche_vs_snowball": snowball["total_months"] - avalanche["total_months"],
                "interest_saved_avalanche_vs_snowball": round(snowball["total_interest_paid"] - avalanche["total_interest_paid"], 2)
            }
        }
    
    def _generate_action_steps(self, analysis: Dict, problems: List[Dict], method: Dict) -> List[Dict]:
        """Generate specific action steps"""
        steps = []
        
        # Immediate actions
        steps.append({
            "priority": "immediate",
            "title": "Stop Accumulating New Debt",
            "description": "Immediately stop using credit cards and taking new loans. This is critical to breaking the debt cycle.",
            "timeline": "Today"
        })
        
        steps.append({
            "priority": "immediate",
            "title": "Set Up Automatic Payments",
            "description": "Set up automatic minimum payments for all debts to avoid late fees and credit score damage.",
            "timeline": "Within 48 hours"
        })
        
        # Week 1 actions
        steps.append({
            "priority": "week_1",
            "title": "Create a Detailed Budget",
            "description": f"Track every expense. You have ${analysis['extra_payment_capacity']:.2f} extra per month. Find ways to increase this.",
            "timeline": "Week 1"
        })
        
        if any(p["type"] == "High Interest Rates" for p in problems):
            steps.append({
                "priority": "week_1",
                "title": "Explore Balance Transfer Options",
                "description": "Research 0% APR balance transfer credit cards for high-interest debts. This could save you thousands.",
                "timeline": "Week 1-2"
            })
        
        # Month 1 actions
        steps.append({
            "priority": "month_1",
            "title": "Implement the " + method["method_name"],
            "description": f"Follow the {method['method_name']} to become debt-free in {method['time_to_debt_free']}.",
            "timeline": "Month 1 onwards"
        })
        
        steps.append({
            "priority": "month_1",
            "title": "Build a Small Emergency Fund",
            "description": "Save $500-1000 for emergencies to avoid taking on new debt when unexpected expenses arise.",
            "timeline": "Month 1-3"
        })
        
        # Ongoing actions
        steps.append({
            "priority": "ongoing",
            "title": "Increase Income or Decrease Expenses",
            "description": "Every extra $100/month could reduce your debt-free date by several months. Consider side hustles or cutting expenses.",
            "timeline": "Ongoing"
        })
        
        steps.append({
            "priority": "ongoing",
            "title": "Review Progress Monthly",
            "description": "Track your progress monthly. Celebrate milestones! This keeps you motivated.",
            "timeline": "Monthly review"
        })
        
        if analysis["budget_utilization_percentage"] > 50:
            steps.append({
                "priority": "immediate",
                "title": "Consider Professional Help",
                "description": "Your debt-to-income ratio is high. Consider speaking with a non-profit credit counselor.",
                "timeline": "Week 1"
            })
        
        return steps
    
    def _generate_milestones(self, method: Dict) -> List[Dict]:
        """Generate milestone celebrations"""
        milestones = []
        
        if method["payoff_timeline"]:
            # First debt payoff
            first_payoff = method["payoff_timeline"][0]
            milestones.append({
                "title": f"First Victory: {first_payoff['debt_name']} Paid Off!",
                "timeline": first_payoff["years_months"],
                "description": "Your first debt eliminated! This momentum will carry you forward.",
                "celebration": "Treat yourself to something small (under $50) to celebrate!"
            })
            
            # Halfway point
            halfway = len(method["payoff_timeline"]) // 2
            if halfway > 0 and halfway < len(method["payoff_timeline"]):
                halfway_payoff = method["payoff_timeline"][halfway]
                milestones.append({
                    "title": "Halfway There!",
                    "timeline": halfway_payoff["years_months"],
                    "description": "You've paid off half your debts. The finish line is in sight!",
                    "celebration": "Celebrate with a debt-free activity (picnic, game night, etc.)"
                })
            
            # Final payoff
            final_payoff = method["payoff_timeline"][-1]
            milestones.append({
                "title": "DEBT FREE!!!",
                "timeline": final_payoff["years_months"],
                "description": "You did it! You're completely debt-free and ready for financial freedom!",
                "celebration": "Major celebration! You've changed your life!"
            })
        
        # Additional milestones
        total_debt = sum(d.balance for d in self.debts)
        milestones.append({
            "title": "25% Debt Eliminated",
            "timeline": f"~{method['total_months'] // 4} months",
            "description": f"You've paid off ${total_debt * 0.25:,.2f} of your debt!",
            "celebration": "Share your success with a supportive friend or family member"
        })
        
        return milestones
    
    def _generate_tips(self, analysis: Dict) -> List[str]:
        """Generate helpful tips"""
        tips = [
            "Always pay more than the minimum payment when possible - even $50 extra makes a huge difference",
            "Use windfalls wisely: Apply tax refunds, bonuses, or gifts directly to debt",
            "Cut expenses: Small changes like cooking at home or canceling unused subscriptions can free up debt payment money",
            "Avoid new debt: Remove credit card info from online shopping sites to reduce impulse purchases",
            "Stay motivated: Visualize your debt-free life and remind yourself why you're doing this",
            "Track your progress: Use a debt payoff chart or app to see your progress visually",
            "Negotiate: Call creditors to negotiate lower interest rates - you'd be surprised how often this works",
            "Sell unused items: Declutter your home and put that money toward debt",
            "Automate payments: Set up automatic payments so you never miss a payment",
            "Reward yourself (wisely): Celebrate milestones with free or low-cost rewards"
        ]
        
        # Add specific tips based on situation
        if analysis["extra_payment_capacity"] < 100:
            tips.insert(0, "PRIORITY: Look for ways to increase income or reduce expenses to accelerate debt payoff")
        
        if analysis["weighted_avg_interest_rate"] > 18:
            tips.insert(0, "URGENT: Your average interest rate is very high. Explore balance transfers or debt consolidation immediately")
        
        return tips


def process_debt_analysis(debt_data: List[Dict], monthly_budget: float) -> Dict[str, Any]:
    """
    Main function to process debt analysis
    
    Args:
        debt_data: List of debt dictionaries with keys: name, balance, interest_rate, minimum_payment, debt_type
        monthly_budget: Monthly budget available for debt repayment
    
    Returns:
        Complete debt analysis and roadmap
    """
    # Convert to Debt objects
    debts = [
        Debt(
            name=d["name"],
            balance=float(d["balance"]),
            interest_rate=float(d["interest_rate"]),
            minimum_payment=float(d["minimum_payment"]),
            debt_type=d.get("debt_type", "other")
        )
        for d in debt_data
    ]
    
    # Generate roadmap
    roadmap_gen = RoadmapGenerator(debts, monthly_budget)
    result = roadmap_gen.generate_roadmap()
    
    return result


# Example usage
if __name__ == "__main__":
    # Sample debt data
    sample_debts = [
        {
            "name": "Credit Card 1",
            "balance": 5000,
            "interest_rate": 19.99,
            "minimum_payment": 150,
            "debt_type": "credit_card"
        },
        {
            "name": "Credit Card 2",
            "balance": 3000,
            "interest_rate": 24.99,
            "minimum_payment": 90,
            "debt_type": "credit_card"
        },
        {
            "name": "Personal Loan",
            "balance": 8000,
            "interest_rate": 12.5,
            "minimum_payment": 250,
            "debt_type": "personal_loan"
        },
        {
            "name": "Car Loan",
            "balance": 12000,
            "interest_rate": 6.5,
            "minimum_payment": 350,
            "debt_type": "auto_loan"
        }
    ]
    
    monthly_budget = 1200
    
    result = process_debt_analysis(sample_debts, monthly_budget)
    print(json.dumps(result, indent=2))
