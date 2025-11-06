require Rails.root.join('app/services/twilio_service.rb')
require Rails.root.join('lib/in_memory_store.rb')

class CallManager
  def initialize
    @twilio = TwilioService.new
  end

  # === Generate 100 random Indian toll-free numbers ===
  def generate_indian_numbers(count = 100)
    Array.new(count) { "1800#{rand(100000..999999)}" }
  end

  def start_campaign(numbers, command = "Default call message")
    raise ArgumentError, "No numbers provided" if numbers.blank?

    results = []

    numbers.each do |num|
      result = @twilio.make_call(num, command)
      MEMORY_STORE.add_log(
        number: num,
        action: 'call',
        command: command,
        status: result[:status],
        duration: result[:duration]
      )
      results << result
      sleep(1.0) # small delay between calls to simulate pacing
    end

    {
      success: true,
      count: results.size,
      completed: results.count { |r| r[:status] == 'completed' },
      failed: results.count { |r| r[:status] == 'failed' },
      calls: results
    }
  rescue => e
    {
      success: false,
      error: e.message,
      backtrace: e.backtrace[0..5]
    }
  end
end
