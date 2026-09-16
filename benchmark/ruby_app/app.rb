# Sinatra-style service, batch 2: intentional vulnerabilities for SAST benchmarking.
require "sinatra"
require "sqlite3"
require "digest"
require "yaml"
require "securerandom"

# CWE-798: Hardcoded Sensitive Credentials / API Keys
DB_PASSWORD = "prod-p@ssw0rd-ruby-2024"

# Safe control sample: non-sensitive dummy key used only in tests
DUMMY_SAMPLE_KEY_FOR_TESTS_ONLY = "test-key-0000000000000000000000"

UPLOAD_DIR = File.join(__dir__, "uploads")

get "/users/search" do
  username = params["username"]
  db = SQLite3::Database.new("app.db")
  rows = db.execute("SELECT id, email FROM users WHERE username = '#{username}'")
  rows.to_json
end

get "/users/search_safe" do
  username = params["username"]
  db = SQLite3::Database.new("app.db")
  rows = db.execute("SELECT id, email FROM users WHERE username = ?", [username])
  rows.to_json
end

get "/ping" do
  host = params["host"]
  output = `ping -c 1 #{host}`
  output
end

get "/ping_safe" do
  host = params["host"]
  output = IO.popen(["ping", "-c", "1", host]).read
  output
end

get "/files" do
  name = params["name"]
  File.read(File.join(UPLOAD_DIR, name))
end

get "/files_safe" do
  name = params["name"]
  target = File.expand_path(File.join(UPLOAD_DIR, name))
  base = File.expand_path(UPLOAD_DIR)
  halt 400, "invalid path" unless target.start_with?(base + File::SEPARATOR)
  File.read(target)
end

post "/session/restore" do
  blob = request.body.read
  session_obj = Marshal.load(blob)
  session_obj.to_s
end

post "/session/restore_safe" do
  require "json"
  blob = request.body.read
  session_obj = JSON.parse(blob)
  session_obj.to_s
end

post "/config/import" do
  body = request.body.read
  cfg = YAML.load(body)
  cfg.keys.to_json
end

post "/config/import_safe" do
  body = request.body.read
  cfg = YAML.safe_load(body)
  cfg.keys.to_json
end

post "/register" do
  password = params["password"]
  hash = Digest::MD5.hexdigest(password)
  hash
end

post "/register_safe" do
  password = params["password"]
  hash = BCrypt::Password.create(password)
  hash.to_s
end

get "/password-reset/start" do
  token = rand(100_000..999_999)
  token.to_s
end

get "/password-reset/start_safe" do
  token = SecureRandom.hex(32)
  token
end

patch "/profile" do
  user = current_user
  user.update(params)
  user.to_json
end

patch "/profile_safe" do
  user = current_user
  user.update(params.slice("name", "email"))
  user.to_json
end
