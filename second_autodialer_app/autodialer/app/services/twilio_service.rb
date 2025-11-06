require 'twilio-ruby'
require 'securerandom'

class TwilioService
  def initialize
    @account_sid = ENV.fetch('TWILIO_ACCOUNT_SID', nil)
    @auth_token  = ENV.fetch('TWILIO_AUTH_TOKEN', nil)
    @caller_id   = ENV.fetch('TWILIO_CALLER_ID', '+15005550006')
    @real_call   = ENV.fetch('REAL_CALL', 'false').to_s.downcase == 'true'
  end

  # === Public entry point ===
  def make_call(to_number, command = nil)
    # Fallback to simulation if real mode is disabled
    return simulate_call(to_number, command) unless @real_call

    begin
      validate_credentials!

      client = Twilio::REST::Client.new(@account_sid, @auth_token)

      # Generate dynamic TwiML with the provided command text
      twiml = generate_twiml(command)
      twiml_url = upload_twiml_to_vercel(twiml)

      call = client.calls.create(
        from: @caller_id,
        to: format_number(to_number),
        url: twiml_url
      )

      {
        sid: call.sid,
        status: call.status || 'initiated',
        duration: 0,
        to: to_number,
        from: @caller_id,
        mode: 'real',
        command: command
      }

    rescue => e
      {
        sid: 'ERROR',
        status: 'failed',
        duration: 0,
        error: e.message,
        mode: 'real',
        command: command
      }
    end
  end

  # === Generate dynamic TwiML ===
  def generate_twiml(command = nil)
    message = if command && !command.strip.empty?
      # Slightly reword user message for natural tone
      "Hello, this is an automated call from Autodialer. #{command.strip.capitalize}."
    else
      "Hello, this is an automated call from Autodialer. Thank you for your time."
    end

    <<~TWIML
      <Response>
        <Say voice="alice" language="en-IN">
          #{message}
        </Say>
      </Response>
    TWIML
  end

  private

  # === Simulated (mock) call ===
  def simulate_call(to_number, command = nil)
    call_sid = "CA#{SecureRandom.hex(16)}"
    sleep(0.3)

    # 85% success, 15% failure
    status = rand > 0.15 ? 'completed' : 'failed'
    duration = status == 'completed' ? rand(30..120) : 0

    {
      sid: call_sid,
      status: status,
      duration: duration,
      to: to_number,
      from: @caller_id,
      mode: 'mock',
      command: command
    }
  end

  # === Helpers ===
  def validate_credentials!
    raise 'Missing TWILIO_ACCOUNT_SID' if @account_sid.nil? || @account_sid.empty?
    raise 'Missing TWILIO_AUTH_TOKEN' if @auth_token.nil? || @auth_token.empty?
  end

  def format_number(num)
    num = num.to_s.strip
    # Basic Indian number normalization
    if num.start_with?('+91')
      num
    elsif num.length == 10
      "+91#{num}"
    else
      num
    end
  end
end
