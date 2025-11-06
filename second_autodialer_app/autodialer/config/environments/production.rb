require "active_support/core_ext/integer/time"

Rails.application.configure do
  # Code is not reloaded between requests.
  config.enable_reloading = false

  # Eager load code on boot for better performance.
  config.eager_load = true

  # Disable full error reports in production.
  config.consider_all_requests_local = false

  # Enable server timing.
  config.server_timing = true

  # Use memory store cache (simple for small apps).
  config.cache_store = :memory_store

  # Serve static files (important for Vercel, Render, etc.)
  config.public_file_server.enabled = ENV["RAILS_SERVE_STATIC_FILES"].present? || true

  # Enable response compression for faster load times.
  config.middleware.use Rack::Deflater

  # Use standard logging.
  config.log_level = :info
  config.log_tags = [:request_id]

  # Use default logging formatter.
  config.log_formatter = ::Logger::Formatter.new

  # Send logs to STDOUT if environment variable is set (for cloud platforms).
  if ENV["RAILS_LOG_TO_STDOUT"].present?
    logger = ActiveSupport::Logger.new(STDOUT)
    logger.formatter = config.log_formatter
    config.logger = ActiveSupport::TaggedLogging.new(logger)
  end

  # Disable deprecation warnings in production logs.
  config.active_support.report_deprecations = false
end
