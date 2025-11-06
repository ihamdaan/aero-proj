class CallLog
  attr_accessor :number, :status, :duration, :timestamp, :sid

  def initialize(number:, status: 'pending', duration: 0, sid: nil)
    @number = number
    @status = status
    @duration = duration
    @timestamp = Time.now
    @sid = sid || "CA#{SecureRandom.hex(16)}"
  end

  def to_h
    {
      number: @number,
      status: @status,
      duration: @duration,
      timestamp: @timestamp.strftime('%Y-%m-%d %H:%M:%S'),
      sid: @sid
    }
  end
end