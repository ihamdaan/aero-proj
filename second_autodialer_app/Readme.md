# second_autodialer_app

A comprehensive Ruby on Rails application integrated with AI-powered capabilities for automated phone dialing and personalized blog content generation. This project combines traditional telephony services with modern AI interfaces to create an intelligent autodialer system that can process natural language commands and manage bulk calling operations.

The application features two main components: an autodialer system with call logging and analytics, and a dynamic blog section with AI-generated content. Both systems are designed with modularity and reusability in mind, making it easy to extend and customize for various use cases.

## Project Overview

The second_autodialer_app was built to solve a common problem in outreach and communication workflows: the need to make automated calls to large lists of contacts while maintaining detailed logs and analytics. Beyond simple automation, this project integrates AI capabilities that allow users to initiate calls through natural language prompts like "call +91 1800 123 4567 with a reminder about the meeting."

The application is structured as two independent but interconnected services:

1. **Main Rails Application** (`autodialer/`) - Handles the web interface, call management, Twilio integration, and blog content display
2. **LLM Service** (`llm_service/`) - A FastAPI microservice that processes natural language commands and extracts structured calling instructions

This architecture allows the Ruby application to focus on business logic and telephony operations while delegating AI processing to a specialized Python service optimized for language model interactions.

## Key Features

### Autodialer Functionality

- **Bulk Call Management** - Upload or paste up to 100 phone numbers for automated calling
- **AI-Powered Commands** - Use natural language like "make a call to +91 1800 555 0123" instead of filling forms
- **Real-time Call Logging** - Track which calls were answered, failed, busy, or went to voicemail
- **Twilio Integration** - Professional telephony infrastructure with configurable voice scripts
- **Test Environment** - Uses Twilio test credentials by default to prevent accidental real calls
- **Modular Architecture** - Each dialer feature is built as a reusable component

### Blog System

- **Dynamic Content Generation** - Integrates with the `third_personalizedContent_app` for AI-written blog posts
- **Dynamic Routing** - Single route handles all blog pages without individual route definitions
- **SEO Optimization** - Generated content follows SEO best practices
- **Smooth Navigation** - No page reloads, seamless content loading

### Technical Highlights

- **Tailwind CSS Styling** - Modern, responsive design system
- **Modular Codebase** - Components designed for reusability and maintenance
- **Environment-Based Configuration** - Easy switching between test and production modes
- **Comprehensive Error Handling** - Graceful failure management for API calls and telephony operations

## Architecture

### Main Application (Ruby on Rails)

The Rails application serves as the primary interface and orchestration layer. It handles:

- User interface rendering with Tailwind CSS
- Phone number input (bulk upload or manual entry)
- Integration with Twilio API for making actual calls
- Communication with the LLM service for natural language processing
- Call status tracking and analytics display
- Blog content fetching and rendering

### LLM Service (FastAPI + Python)

This microservice processes natural language commands and extracts structured data:

- Accepts text prompts from the Rails application
- Uses Mistral 7B Instruct model via OpenRouter
- Extracts action, phone number, and message from user input
- Validates and formats phone numbers automatically
- Returns structured JSON for the Rails app to process

The separation allows the Ruby application to remain focused on web and telephony logic while Python handles the complexities of AI model integration.

## Highlighted Project Structure

```
second_autodialer_app/
│
├── autodialer/                    # Main Ruby on Rails application
│   ├── app/
│   │   ├── controllers/           # Request handling and business logic
│   │   ├── models/                # Data models and validations
│   │   ├── views/                 # UI templates with Tailwind CSS
│   │   └── services/              # Twilio integration and external API calls
│   ├── config/
│   │   └── routes.rb              # Dynamic routing configuration
│   ├── Gemfile                    # Ruby dependencies
│   └── .env.example               # Environment configuration template
│
└── llm_service/                   # FastAPI microservice for AI processing
    ├── main.py                    # FastAPI application and endpoint
    ├── utils/
    │   └── parser.py              # Pydantic models and response parsing
    ├── requirements.txt           # Python dependencies
    └── .env.example               # API key configuration template
```

## Installation & Setup

### Prerequisites

- Ruby 3.x and Rails 8.1.1+
- Python 3.8+
- Node.js (for Tailwind CSS compilation)
- Twilio account (free tier works for testing)
- OpenRouter API key (free tier available)

### Setting Up the Main Rails Application

1. **Clone the repository**

```bash
git clone https://github.com/ihamdaan/aero-proj.git
cd second_autodialer_app/autodialer
```

2. **Install Ruby dependencies**

```bash
bundle install
```

3. **Install Tailwind CSS**

```bash
rails tailwindcss:install
```

4. **Configure environment variables**

Copy `.env.example` to `.env` and configure:

```
TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID_HERE
TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN_HERE
TWILIO_CALLER_ID=YOUR_TWILIO_CALLER_ID_HERE
AI_PROMPT_API_URL=https://your-llm-service-url.vercel.app/prompt
AI_BLOG_API_URL=https://your-blog-service-url.vercel.app/personalizedcontent
RAILS_ENV=production
REAL_CALL=false
```

**Important:** Keep `REAL_CALL=false` during testing to use Twilio's test environment. Set to `true` only when making actual calls.

5. **Setup database**

```bash
rails db:create db:migrate
```

6. **Start the Rails server**

```bash
rails server
```

The application will be available at `http://localhost:3000`

### Setting Up the LLM Service

1. **Navigate to the service directory**

```bash
cd ../llm_service
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure API key**

Copy `.env.example` to `.env`:

```
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY_HERE
```

Get a free API key from https://openrouter.ai/

5. **Start the FastAPI service**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

The service will be available at `http://localhost:8001`

## Using the Application

### Making Calls via Bulk Upload

1. Navigate to the autodialer interface
2. Upload a CSV file or paste phone numbers (one per line)
3. Configure call settings (voice message, timing, etc.)
4. Click "Start Dialing"
5. Monitor real-time call status in the logs panel

### Making Calls via AI Prompt

1. Go to the AI prompt interface
2. Type or speak commands like:
   - "Call +91 1800 555 0123"
   - "Make a call to 1800-TESTING and say the meeting is at 3 PM"
   - "Dial +1 800 555 0199 with a delivery notification"
3. The system extracts the number and message automatically
4. Review and confirm before initiating the call

### Testing Safely

Always use Twilio's test numbers during development:
- **US Test Numbers:** +1 800 XXX XXXX format
- **India Test Numbers:** +91 1800 XXX XXXX format

These numbers simulate call behavior without actually connecting to real phones, preventing accidental calls to real people.

## Key Dependencies

### Ruby Gems (Main Application)

- **rails** (~> 8.1.1) - Web application framework
- **twilio-ruby** (~> 6.0) - Twilio API integration
- **httparty** (~> 0.21) - HTTP client for external API calls
- **tailwindcss-rails** - Modern CSS framework
- **turbo-rails** - SPA-like page acceleration
- **stimulus-rails** - JavaScript framework
- **dotenv-rails** - Environment variable management

### Python Packages (LLM Service)

- **fastapi** - Modern API framework
- **requests** - HTTP library for OpenRouter API
- **pydantic** - Data validation and parsing
- **python-dotenv** - Environment configuration

## How the AI Integration Works

When a user submits a natural language command:

1. The Rails application sends the text to the LLM service's `/prompt` endpoint
2. The FastAPI service constructs a specialized prompt for the Mistral 7B model
3. OpenRouter processes the request and returns structured extraction
4. The parser validates phone numbers and extracts action/message
5. Structured JSON is returned to Rails with: `{action, number, command}`
6. Rails uses this data to initiate the Twilio call with the appropriate script

This workflow allows non-technical users to interact with the system naturally while maintaining strict data validation and error handling.

## Call Logging and Analytics

The application tracks comprehensive metrics for each calling session:

- **Total Calls Attempted** - Number of numbers dialed
- **Successful Connections** - Calls that were answered
- **Failed Calls** - Numbers that didn't connect (wrong number, network issues)
- **Busy Signals** - Lines that were occupied
- **Voicemail** - Calls that went to automated systems
- **Call Duration** - Length of each connected call
- **Timestamps** - Precise timing for audit trails

All logs are stored in the database and displayed in real-time on the dashboard.

## Deployment Considerations

### Main Rails Application

Best deployed on Ruby-friendly platforms:
- **Heroku** - Simple Rails deployment with add-ons
- **Render** - Modern platform with free tier
- **Railway** - Easy configuration and scaling

### LLM Service

Best deployed on Python-optimized platforms:
- **Vercel** - Serverless functions, excellent for FastAPI
- **Railway** - Good Python support
- **Render** - Free tier with persistent processes

Both services should be deployed independently to leverage platform-specific optimizations and free tier benefits.

## Security and Privacy

- **Test Mode Default** - Prevents accidental real calls
- **Environment Variables** - Sensitive credentials never hardcoded
- **API Key Rotation** - Easy to update without code changes
- **Call Logging** - Audit trails for compliance
- **Input Validation** - Prevents injection attacks and malformed data

## Ethical Usage

This tool is designed for legitimate business use cases such as:
- Appointment reminders
- Delivery notifications
- Survey outreach with consent
- Customer service callbacks

**Do not use for:**
- Unsolicited marketing (spam)
- Harassment or threats
- Robocalling without consent
- Violating Do Not Call registries

Always comply with local telecommunications regulations and obtain appropriate consent before making automated calls.

## Conclusion

The second_autodialer_app demonstrates how modern web applications can integrate traditional telephony systems with cutting-edge AI capabilities. By separating concerns into specialized services and leveraging the strengths of both Ruby and Python ecosystems, the application achieves a balance of simplicity, power, and maintainability.

Whether you need to manage bulk calling campaigns or simply want to experiment with AI-driven telephony interfaces, this project provides a solid foundation that's both educational and production-ready.