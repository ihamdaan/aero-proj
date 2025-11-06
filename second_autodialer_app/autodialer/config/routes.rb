Rails.application.routes.draw do
  # Default homepage → Dialer
  root "dialer#index"

  # === Dialer Routes ===
  get  "dialer",                  to: "dialer#index"
  post "dialer/upload_numbers",   to: "dialer#upload_numbers"
  post "dialer/start_campaign",   to: "dialer#start_campaign"
  post "dialer/stop_campaign",    to: "dialer#stop_campaign"
  post "dialer/clear_logs",       to: "dialer#clear_logs"
  post "dialer/ai_prompt",        to: "dialer#ai_prompt"
  get  "dialer/call_logs",        to: "dialer#call_logs"
  get  "dialer/get_numbers",      to: "dialer#get_numbers"

  # === Blog Routes ===
  get  "blogs",                   to: "blogs#index"
  get "view_blogpost/:id", to: "view_blogposts#show", as: "view_blogpost"

  # === Personalized Content Routes ===
  get  "personalizedcontent",          to: "personalizedcontent#index"
  post "personalizedcontent/generate", to: "personalizedcontent#generate"
end