require 'json'
require 'net/http'
require Rails.root.join('lib/in_memory_store.rb')
require Rails.root.join('app/services/ai_prompt_service.rb')
require Rails.root.join('app/services/twilio_service.rb')
require Rails.root.join('app/services/call_manager.rb')

class DialerController < ApplicationController
  protect_from_forgery with: :null_session

  # === BASIC ROUTES ===
  def index
    @call_logs = MEMORY_STORE.get_call_logs
  end

  # === Upload numbers manually or generate random ===
  def upload_numbers
    numbers_text = params[:numbers]

    if numbers_text.present?
      numbers = numbers_text.split("\n").map(&:strip).reject(&:blank?)
      MEMORY_STORE.set_numbers(numbers)
      render json: { success: true, count: numbers.count }
    else
      # Use CallManager to generate random numbers
      manager = CallManager.new
      numbers = manager.generate_indian_numbers(100)
      MEMORY_STORE.set_numbers(numbers)
      render json: { success: true, count: numbers.count, generated: true }
    end
  end

  # === Start campaign ===
  def start_campaign
    numbers = MEMORY_STORE.get_numbers
    command = params[:command].presence || "Default call message"

    if numbers.empty?
      render json: { error: 'No numbers loaded' }, status: :unprocessable_entity
      return
    end

    manager = CallManager.new
    result = manager.start_campaign(numbers, command)

    render json: result
  end

  # === AI Prompt handler ===
  def ai_prompt
    text = params[:text]

    if text.blank?
      render json: { success: false, error: 'No text provided' } and return
    end

    begin
      # Step 1: Send text to AI service
      ai = AiPromptService.new
      puts "Text: #{text}"
      prompt_result = ai.process_prompt(text)
      puts "AI Prompt Result: #{prompt_result.inspect}"
      action_info = ai.extract_action(prompt_result)

      # Step 2: Ensure valid action and number
      if action_info.present? && action_info['number'].present?
        number  = action_info['number']
        command = action_info['command']

        # Step 3: Trigger Twilio or your dialer simulation
        twilio = TwilioService.new
        result = twilio.make_call(number, command)

        # Step 4: Save to memory store (log)
        MEMORY_STORE.add_log(
          number: number,
          action: 'call',
          command: command,
          status: result[:status],
          duration: result[:duration]
        )

        # Step 5: Respond
        render json: {
          success: true,
          number: number,
          command: command,
          call_log: result,
          message: "Simulated call #{result[:status]} for #{number}"
        }
      else
        render json: {
          success: false,
          message: "AI didn’t return a valid call command",
          ai_output: prompt_result
        }
      end

    rescue => e
      render json: {
        success: false,
        error: e.message,
        backtrace: e.backtrace[0..5]
      }, status: :internal_server_error
    end
  end

  # === Retrieve logs ===
  def call_logs
    logs = MEMORY_STORE.get_call_logs
    render json: { logs: logs }
  end

  # === Retrieve stored numbers ===
  def get_numbers
    numbers = MEMORY_STORE.get_numbers
    render json: { numbers: numbers }
  end

  # === Clear memory logs ===
  def clear_logs
    MEMORY_STORE.clear_logs
    MEMORY_STORE.set_numbers([])
    render json: { success: true, message: 'Logs cleared' }
  end

  def stop_campaign
    MEMORY_STORE.set(:campaign_stopped, true)
    render json: { success: true, message: "Campaign stopped manually" }
  end

end
