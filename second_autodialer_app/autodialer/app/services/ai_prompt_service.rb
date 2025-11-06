require 'httparty'

class AiPromptService
  def initialize
    @api_url = ENV.fetch('AI_PROMPT_API_URL')
  end

  def process_prompt(text)
    response = HTTParty.post(
      @api_url,
      body: { text: text }.to_json,
      headers: { 'Content-Type' => 'application/json' },
      timeout: 35
    )

    puts "API Output: #{response.body}"
    if response.success?
      JSON.parse(response.body)
    else
      { 'error' => 'AI API request failed', 'status' => response.code }
    end
  rescue => e
    { 'error' => e.message }
  end

  def extract_action(prompt_result)
    return nil unless prompt_result['action'] == 'call'
    {
      'number' => prompt_result['number'],
      'command' => prompt_result['command']
    }
  end
end