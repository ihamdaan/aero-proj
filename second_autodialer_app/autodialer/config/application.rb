require_relative "boot"
require "rails"
require "action_controller/railtie"
require "action_view/railtie"
require "active_model/railtie"

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
