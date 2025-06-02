from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
load_dotenv()
def get_company_symbol(company: str) -> str:
    """Use this function to get the symbol for a company.

    Args:
        company (str): The name of the company.

    Returns:
        str: The symbol for the company.
    """
    symbols = {
        "Phidata": "MSFT",
        "Infosys": "INFY",
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL",
    }
    return symbols.get(company, "Unknown")

agent = Agent(
    model=Groq(id="qwen-qwq-32b"),
    tools=[
        YFinanceTools(stock_price=True, stock_fundamentals=True, analyst_recommendations=True),
        get_company_symbol
        ],
    show_tool_calls=True,
    markdown=True,
    instructions=["Use tables to present data clearly.", 
                  "If you don't know the company symbol, use the get_company_symbol function to find it. Even if it is not a public company, you can still use the function to get the symbol.",],
    
)
agent.print_response("Summerize and compare analyst recommedations and fundamentals for Apple and Phidata. Which stock is a better buy?")  # type: ignore
