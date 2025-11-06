require_relative "boot"
require "rails"
require "action_controller/railtie"
require "action_view/railtie"

require_relative "../lib/in_memory_store"

Bundler.require(*Rails.groups)

module Autodialer
  class Application < Rails::Application
    config.load_defaults 7.1
    config.api_only = false
    
    # Disable ActiveRecord
    config.generators.orm false
    
    # Load lib directory
    config.autoload_paths << Rails.root.join('lib')
    config.eager_load_paths << Rails.root.join('lib')
  end
end