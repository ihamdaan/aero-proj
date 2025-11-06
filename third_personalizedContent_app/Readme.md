# third_personalizedContent_app

A FastAPI-based microservice that generates personalized, SEO-optimized blog content using free open-source language models via OpenRouter. This service is designed to handle bulk content generation requests with precise word count control and professional styling.

This application is deployed as a standalone Python service, separate from the main Ruby application, allowing each component to leverage the best deployment platform for its respective technology stack.

## Project Overview

The third_personalizedContent_app serves as a specialized content generation microservice that accepts structured input about content requirements and returns professionally written blog posts. It handles everything from parsing user requests to managing API interactions with OpenRouter's free models.

The service processes multiple content requests in a single API call, making it efficient for bulk content generation workflows. Each generated piece includes actual word count tracking to ensure transparency and quality control.

Key features include:

- **Batch Processing** – Generate multiple blog posts in a single request
- **Word Count Control** – Request specific lengths and track actual output
- **SEO Optimization** – Content generated with SEO best practices in mind
- **Free Model Integration** – Uses OpenRouter's free tier (gpt-oss-20b) to minimize costs
- **Error Resilience** – Graceful handling of API failures with proper logging
- **Type Safety** – Pydantic models ensure data validation and structure

## Why Separate Deployment?

This service is deployed independently from the main application for several strategic reasons:

1. **Technology Stack Isolation** – The main application is built with Ruby, while this service leverages Python's rich ecosystem for AI/ML integrations
2. **Platform Optimization** – Each service can be deployed on platforms optimized for their respective languages (e.g., Heroku for Ruby, Railway/Render for Python)
3. **Scalability** – Content generation can scale independently based on demand without affecting the main application
4. **Development Flexibility** – Teams can update and deploy the content service without touching the main codebase
5. **Cost Efficiency** – Different deployment platforms offer different free tiers; separating services maximizes free tier benefits

## Project Structure

```
third_personalizedContent_app/
│
├── main.py                 # FastAPI application and endpoint logic
├── utils/
│   └── parser.py           # Pydantic models for request/response validation
│
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment configuration
└── README.md               # This documentation
```

## How It Works

The service exposes a single POST endpoint `/personalizedcontent` that accepts a JSON payload containing multiple content requests. For each request, it:

1. Validates the input structure using Pydantic models
2. Constructs an optimized prompt for the language model
3. Sends the request to OpenRouter's API using the free gpt-oss-20b model
4. Calculates the actual word count of generated content
5. Returns structured results with titles, content, and metadata

The ContentItem model defines the input structure with fields for title, description, and desired word length. The PersonalizedContent model structures the output with the generated content and actual word count.

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/ihamdaan/aero-proj.git
cd third_personalizedContent_app
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # for macOS/Linux
venv\Scripts\activate     # for Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The requirements.txt includes:
- fastapi – Modern web framework for building APIs
- requests – HTTP library for OpenRouter API calls
- pydantic – Data validation using Python type hints
- python-dotenv – Environment variable management

### 4. Configure environment variables

Copy `.env.example` to `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY_HERE
```

To get a free API key, visit https://openrouter.ai/ and sign up. The service uses the free gpt-oss-20b model which doesn't require payment.

## Running the Service

### Development Mode

Run the FastAPI server locally:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The service will be available at `http://localhost:8000`

### Making Requests

Send a POST request to `/personalizedcontent` with the following structure:

```json
{
  "items": [
    {
      "title": "Introduction to FastAPI",
      "description": "A beginner-friendly guide explaining what FastAPI is and why it's popular",
      "word_length": 500
    },
    {
      "title": "Python vs Ruby",
      "description": "Comparing two popular programming languages for web development",
      "word_length": 800
    }
  ]
}
```

### Response Format

The service returns structured JSON with generated content:

```json
{
  "results": [
    {
      "title": "Introduction to FastAPI",
      "content": "FastAPI is a modern, fast web framework...",
      "word_count_doc": 487
    },
    {
      "title": "Python vs Ruby",
      "content": "When choosing a programming language...",
      "word_count_doc": 792
    }
  ]
}
```

## Deployment

This service is designed to be deployed on Python-friendly platforms. Recommended options include:

- **Railway** – Simple deployment with automatic HTTPS
- **Render** – Free tier with easy FastAPI support
- **Fly.io** – Global deployment with free allowance
- **PythonAnywhere** – Straightforward Python hosting

Each platform offers environment variable management for secure API key storage.

## Error Handling

The service includes comprehensive error handling:

- **Invalid Input** – Returns detailed error messages for malformed JSON
- **API Failures** – Gracefully handles OpenRouter timeouts or errors
- **Logging** – All requests and errors are logged for debugging

If content generation fails for any item, it returns a placeholder with zero word count while continuing to process other items.

## Technical Decisions

**Why FastAPI?** – Modern Python framework with automatic API documentation, type validation, and high performance

**Why OpenRouter?** – Provides access to multiple open-source models through a single API, with generous free tier

**Why Pydantic?** – Ensures data validation and provides clear structure for API contracts

**Why Separate Service?** – Allows independent scaling and deployment optimization for Ruby and Python components

## Conclusion

The third_personalizedContent_app demonstrates how microservices architecture can leverage the best tools for each task. By separating content generation into a dedicated Python service, the system gains flexibility, scalability, and cost efficiency while maintaining clean integration with the main Ruby application.

This approach is particularly valuable for AI-powered features that benefit from Python's ecosystem while the core application uses a different technology stack.