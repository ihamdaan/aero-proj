require "active_support/core_ext/integer/time"

Rails.application.configure do
  # Reload code on every request — slower but perfect for development.
  config.enable_reloading = true

  # Don’t eager load code on boot.
  config.eager_load = false

  # Show full error reports.
  config.consider_all_requests_local = true

  # Enable server timing.
  config.server_timing = true

  # Enable/disable caching (toggle with rails dev:cache)
  if Rails.root.join("tmp/caching-dev.txt").exist?
    config.action_controller.perform_caching = true
    config.action_controller.enable_fragment_cache_logging = true
    config.public_file_server.headers = {
      "Cache-Control" => "public, max-age=#{2.days.to_i}"
    }
  else
    config.action_controller.perform_caching = false
  end

  # Memory store cache for simplicity
  config.cache_store = :memory_store

  # Print deprecation notices to the Rails logger.
  config.active_support.deprecation = :log

  # Log redirect origins for debugging.
  config.action_dispatch.verbose_redirect_logs = true

  # Suppress logger output for asset requests.
  config.assets.quiet = true

  # Annotate rendered views with filenames.
  config.action_view.annotate_rendered_view_with_filenames = true

  # Raise error when a before_action refers to a missing action.
  config.action_controller.raise_on_missing_callback_actions = true
end
