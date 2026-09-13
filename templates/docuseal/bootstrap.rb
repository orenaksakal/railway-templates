# Initialize before opening HTTP. Never reset credentials on an existing account.
unless User.exists?
  Account.transaction do
    account = Account.create!(name: ENV.fetch('ACCOUNT_NAME', 'My organization'), timezone: 'UTC', locale: 'en')
    account.users.create!(email: ENV.fetch('ADMIN_EMAIL'), password: ENV.fetch('ADMIN_PASSWORD'),
                          first_name: 'Admin', role: User::ADMIN_ROLE)
    account.encrypted_configs.create!(key: EncryptedConfig::APP_URL_KEY, value: ENV.fetch('PUBLIC_URL'))
    account.encrypted_configs.create!(key: EncryptedConfig::ESIGN_CERTS_KEY,
                                      value: GenerateCertificate.call.transform_values(&:to_pem))
    account.account_configs.create!(key: :fulltext_search, value: true) if SearchEntry.table_exists?
  end
end
