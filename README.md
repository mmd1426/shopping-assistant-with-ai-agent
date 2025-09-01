# Shopping Assistant with AI Agent

A FastAPI-based shopping assistant that uses AI agents to search and recommend products from the Basalam marketplace. The application leverages LangChain and OpenAI-compatible models to provide intelligent product search capabilities.

## Features

- AI-powered product search using LangChain agents
- Integration with Basalam marketplace API
- FastAPI REST API with automatic reload
- Docker containerization for easy deployment
- Support for product filtering (price range, rating, free shipping)
- Persian language support for product descriptions

## Prerequisites

- Docker and Docker Compose
- Basalam API token
- OpenRouter API key (for LLM access)

## Environment Variables

Please enter your tokens in the .env file to complete this section.

```env
BASALAM_TOKEN=your_basalam_api_token
LLM_MODEL_API_KEY=your_openrouter_api_key
```

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd shopping-assistant-with-agent
```

2. Create the `.env` file with your API credentials

3. Start the application:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8080`

#### Health Check Configuration

The application includes a health check mechanism that monitors the service status:

- **Test Command**: `curl -f http://localhost:8080/` - Checks if the API is responding
- **Interval**: 30 seconds - How often the health check runs
- **Timeout**: 10 seconds - Maximum time to wait for a response
- **Retries**: 3 attempts - Number of failed attempts before marking as unhealthy
- **Start Period**: 40 seconds - Initial grace period before health checks begin

This ensures the container is automatically restarted if the service becomes unresponsive.

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables

3. Run the application:
```bash
cd src/app
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## API Endpoints

### Health Check
- **GET** `/` - API health check

### Product Search
- **POST** `/search` - Search for products using AI agent

**Request Body:**
```json
{
  "prompt": "یک کیف چرمی با قیمت زیر 3000000 ریال با ارسال رایگان برام پیدا کن"
}
```

**Response:**
```json
{
  "products": [
    "محصول کیف چزم دست دوز پارسه جاموبایلی جاکارتی کیف پول (ارسال رایگان) با قیمت 299000 تومان عرضه می شود. این کالا با امتیاز 4.4 از کاربران، موجود است و دارای ارسال رایگان می باشد",
    "محصول کیف زنانه کیف پاسپورتی زنانه کیف دوشی زنانه ارسال رایگان با قیمت 279300 تومان عرضه می شود. این کالا با امتیاز 4.7 از کاربران، موجود است و دارای ارسال رایگان می باشد",
    "محصول کیف چرم دست دوز (ارسال رایگان) با قیمت 299000 تومان عرضه می شود. این کالا با امتیاز 5.0 از کاربران، موجود است و دارای ارسال رایگان می باشد",
    "محصول کیف دستی زنانه کیف دوشی زنانه کیف پاسپورتی زنانه ارسال رایگان با قیمت 268800 تومان عرضه می شود. این کالا با امتیاز 4.9 از کاربران، موجود است و دارای ارسال رایگان می باشد",
    "محصول کیف زنانه دوشی زنانه ارسال رایگان کیف مجلسی زنانه با قیمت 258300 تومان عرضه می شود. این کالا با امتیاز 4.5 از کاربران، موجود است و دارای ارسال رایگان می باشد"
  ]
}
```

## Project Structure

```
shopping-assistant-with-agent/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── src/
│   └── app/
│       ├── main.py             # FastAPI application entry point
│       ├── create_agent.py     # LangChain agent configuration
│       └── utils/
│           └── utils.py        # Basalam API integration utilities
```

## Technology Stack

- **FastAPI** - Modern web framework for building APIs
- **LangChain** - Framework for developing applications with LLMs
- **OpenRouter** - LLM API gateway (using Llama 3.3 8B model)
- **Basalam SDK** - Official SDK for Basalam marketplace integration
- **Docker** - Containerization platform
- **PyTorch** - Deep learning framework (base image)

## License

This project is licensed under MIT.
