module Api
  class CallsController < ApplicationController
    skip_before_action :verify_authenticity_token

    def voice
      twilio = TwilioService.new
      render xml: twilio.generate_twiml
    end
  end
end
