<?php
$keys = ['dbhostname' => 'DB_HOST', 'dbname' => 'DB_NAME', 'dbusername' => 'DB_USER', 'dbpassword' => 'DB_PASSWORD'];
$content = "<?php\n\$web_root = '';\n";
foreach ($keys as $name => $environment) {
    $value = getenv($environment);
    if ($value === false || $value === '') {
        fwrite(STDERR, "Missing required database variable: $environment\n");
        exit(1);
    }
    $content .= '$' . $name . ' = ' . var_export($value, true) . ";\n";
}
$temporary = '/run/domainmod-config.php.tmp';
if (file_put_contents($temporary, $content) === false || !chmod($temporary, 0640)
    || !chown($temporary, 'www-data') || !rename($temporary, '/run/domainmod-config.php')) {
    fwrite(STDERR, "Cannot initialize DomainMOD configuration\n");
    exit(1);
}
