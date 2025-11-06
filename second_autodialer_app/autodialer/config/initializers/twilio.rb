TWILIO_CONFIG = {
  account_sid: ENV['TWILIO_ACCOUNT_SID'] || 'AC8600b6a8421b8a59',
  auth_token: ENV['TWILIO_AUTH_TOKEN'] || '2f23b913477b46',
  caller_id: ENV['TWILIO_CALLER_ID'] || '+15005550006',
  ai_api_url: ENV['AI_PROMPT_API_URL'] || 'https://autodialer-5iob6kprq-ihamdaans-projects.vercel.app/prompt'
}.freeze
