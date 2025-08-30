# Import required libraries for agent creation
import os
import asyncio
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import StructuredTool
from langchain_openai import ChatOpenAI
from utils.utils import get_product_details
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Get API key from environment
LLM_MODEL_API_KEY = os.getenv("LLM_MODEL_API_KEY")

# Define schema for product search arguments
class ProductSearchArgs(BaseModel):
    query: str = Field(
        description="Search term for products (e.g., mobile phone, laptop, natural honey)",
        examples=["mobile phone", "laptop", "natural honey", "book"]
    )
    minPrice: int = Field(
        default=None,
        description="Minimum product price in Tomans (optional)",
        examples=[100000, 500000, 1000000]
    )
    maxPrice: int = Field(
        default=None,
        description="Maximum product price in Tomans (optional)",
        examples=[5000000, 20000000, 50000000]
    )
    minRating: int = Field(
        default=4,
        description="Minimum product rating out of 5 (default: 3)",
        examples=[3, 4, 5]
    )
    freeShipping: int = Field(
        default=0,
        description="Only products with free shipping (0: all, 1: free shipping only)",
        examples=[0, 1]
    )

# Initialize LLM with OpenRouter API
llm = ChatOpenAI(model="meta-llama/llama-3.3-8b-instruct:free",
                 temperature=0,
                 api_key=LLM_MODEL_API_KEY,
                 base_url="https://openrouter.ai/api/v1"
                 )

# Synchronous wrapper for async product search function
def search_products_sync(query: str, **kwargs):
    """Synchronous product search function"""
    import asyncio
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_product_details(query, **kwargs))
        return result
    finally:
        loop.close()

# Create structured tool for product search
get_product_details_tool = StructuredTool.from_function(
                                     func=search_products_sync,
                                     name="search_products",
                                     description="Search for products using the Basalam API. Use this tool to find products like honey, mobile phones, laptops, etc.",
                                     args_schema=ProductSearchArgs
                                    )

# Define available tools for the agent
tools = [get_product_details_tool]

# System prompt defining agent behavior
system_prompt = """You are Basalam's smart shopping assistant. Your job is to help users find suitable products.

**Important Instructions:**
1. When the user requests a product, use the `search_products` tool only once.
2. Extract the proper parameters:
   - query: product keywords
   - freeShipping: 1 for free shipping
   - minRating: minimum rating (default 4)
   - maxPrice/minPrice: price range
3. After receiving the results, present them to the user and finish the task.
4. Never perform more than one search.

**Examples:**
• "Natural honey" → query: "عسل طبیعی", freeShipping: 1
• "Phone under 15 million" → query: "گوشی", maxPrice: 150000000
• "Laptop with free shipping" → query: "لپ‌تاپ", freeShipping: 1

**Critical Note:** Only perform one search and provide the results. Repetition is strictly forbidden.
"""

# Create prompt template for agent
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create the agent with tools and prompt
agent = create_tool_calling_agent(llm, tools, prompt=prompt_template)

# Create agent executor with configuration
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=False, 
    handle_parsing_errors=True, 
    max_iterations=1,  # Limit to one iteration
    return_intermediate_steps=True
)