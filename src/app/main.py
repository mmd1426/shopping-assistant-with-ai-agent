# Import FastAPI framework and dependencies
from fastapi import FastAPI
from pydantic import BaseModel
from create_agent import agent_executor

# Initialize FastAPI application
app = FastAPI()

# Define data model for user input
class UserInput(BaseModel):
    prompt: str

# API endpoint for product search using AI agent
@app.post("/search")
async def search_products(user_input: UserInput):

    try:
        # Execute agent with user input
        result = await agent_executor.ainvoke({"input": user_input.prompt})

        # Extract final result from agent execution
        final_text = None
        if "intermediate_steps" in result and result["intermediate_steps"]:
            last_step = result["intermediate_steps"][-1]
            if len(last_step) > 1 and isinstance(last_step[1], str):
                final_text = last_step[1]

        # Parse and return product results
        if final_text:
            # Split results into individual product lines
            lines = [line.strip() for line in final_text.split("\n") if line.strip()]
            return {"products": lines}

        return {"products": []}

    except Exception as e:
        # Return error message if something goes wrong
        return {"error": f"System error: {str(e)}"}


# Root endpoint for API health check
@app.get("/")
async def root():
    """Main API page"""
    return {"message": "Basalam Agent API - Use /search to find products"}