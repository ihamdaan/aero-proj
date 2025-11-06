require "active_support/core_ext/integer/time"

Rails.application.configure do
  # The test environment is used exclusively to run the test suite.
  config.enable_reloading = false
  config.eager_load = false

  # Show full error reports.
  config.consider_all_requests_local = true

  # Disable caching for predictability.
  config.action_controller.perform_caching = false
  config.cache_store = :null_store

  # Print deprecation warnings to STDERR.
  config.active_support.deprecation = :stderr

  # Keep logs minimal.
  config.log_level = :warn
end
