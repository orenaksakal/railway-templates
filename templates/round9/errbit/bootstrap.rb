# Never reset a password or run upstream db:seed on restart.
User.create_indexes
if User.count.zero?
  user = User.new(name: 'Administrator', email: ENV.fetch('ERRBIT_ADMIN_EMAIL'), admin: true)
  user.username = ENV.fetch('ERRBIT_ADMIN_USER', 'admin') if Errbit::Config.user_has_username
  user.password = ENV.fetch('ERRBIT_ADMIN_PASSWORD')
  user.password_confirmation = user.password
  user.save!
end
