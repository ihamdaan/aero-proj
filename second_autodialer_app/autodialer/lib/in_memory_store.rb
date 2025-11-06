# lib/in_memory_store.rb
require 'singleton'
require 'time'

class InMemoryStore
  include Singleton

  def initialize
    @call_logs = []
    @numbers = []
  end

  def add_log(number:, status:, duration:, action: nil, command: nil)
    log_entry = {
      number: number,
      action: action,
      command: command,
      status: status,
      duration: duration,
      time: Time.now.strftime("%Y-%m-%d %H:%M:%S")
    }

    @call_logs << log_entry
    @numbers << number unless @numbers.include?(number)
  end

  def get_call_logs
    @call_logs
  end

  def get_numbers
    @numbers
  end

  def clear_logs
    @call_logs = []
  end

  def set_numbers(numbers)
    @numbers = numbers
  end
end

# Make accessible globally (like before)
MEMORY_STORE = InMemoryStore.instance
