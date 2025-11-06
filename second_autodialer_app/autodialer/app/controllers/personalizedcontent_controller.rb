require 'net/http'
require 'json'

class PersonalizedcontentController < ApplicationController
  protect_from_forgery with: :null_session

  def generate
    api_url = ENV.fetch('AI_BLOG_API_URL')
    items = params[:items]

    uri = URI(api_url)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = uri.scheme == 'https'

    request = Net::HTTP::Post.new(uri.path, { 'Content-Type' => 'application/json' })
    request.body = { items: items }.to_json

    response = http.request(request)
    render json: JSON.parse(response.body)
  rescue => e
    render json: { error: "Failed to generate blogs: #{e.message}" }, status: 500
  end
end
