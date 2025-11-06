require_relative "boot"

require "rails/all"

require_relative "../lib/in_memory_store"

Bundler.require(*Rails.groups)

module Autodialer
  class Application < Rails::Application
    config.load_defaults 8.1
    config.api_only = false

    # Load lib directory
    config.autoload_paths << Rails.root.join('lib')
    config.eager_load_paths << Rails.root.join('lib')
  end
end
