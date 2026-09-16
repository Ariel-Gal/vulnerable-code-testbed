<?php
// Plain PHP service, no framework: intentional vulnerabilities for SAST benchmarking.

$DB_HOST = "127.0.0.1";
$DB_USER = "app";
// CWE-798: Hardcoded Sensitive Credentials / API Keys
$DB_PASSWORD = "prod-p@ssw0rd-php-2024";

// Safe control sample: non-sensitive dummy key used only in tests
$DUMMY_SAMPLE_KEY_FOR_TESTS_ONLY = "test-key-0000000000000000000000";

$UPLOAD_DIR = __DIR__ . "/uploads";

$mysqli = new mysqli($DB_HOST, $DB_USER, $DB_PASSWORD, "app_db");

function searchUsers($mysqli) {
    $username = $_GET["username"] ?? "";
    $result = $mysqli->query("SELECT id, email FROM users WHERE username = '" . $username . "'");
    return $result->fetch_all(MYSQLI_ASSOC);
}

function searchUsersSafe($mysqli) {
    $username = $_GET["username"] ?? "";
    $stmt = $mysqli->prepare("SELECT id, email FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
}

function pingHost() {
    $host = $_GET["host"] ?? "";
    $output = shell_exec("ping -c 1 " . $host);
    return $output;
}

function pingHostSafe() {
    $host = $_GET["host"] ?? "";
    $output = shell_exec("ping -c 1 " . escapeshellarg($host));
    return $output;
}

function renderPage() {
    $page = $_GET["page"] ?? "home";
    include $page . ".php";
}

function renderPageSafe() {
    $allowed = ["home", "about", "contact"];
    $page = $_GET["page"] ?? "home";
    if (!in_array($page, $allowed, true)) {
        $page = "home";
    }
    include $page . ".php";
}

function greet() {
    $name = $_GET["name"] ?? "";
    echo "<h1>Welcome, " . $name . "!</h1>";
}

function greetSafe() {
    $name = $_GET["name"] ?? "";
    echo "<h1>Welcome, " . htmlspecialchars($name, ENT_QUOTES) . "!</h1>";
}

function restoreSession() {
    $blob = file_get_contents("php://input");
    $session = unserialize($blob);
    return $session;
}

function restoreSessionSafe() {
    $blob = file_get_contents("php://input");
    $session = json_decode($blob, true);
    return $session;
}

function readFile($UPLOAD_DIR) {
    $name = $_GET["name"] ?? "";
    return file_get_contents($UPLOAD_DIR . "/" . $name);
}

function readFileSafe($UPLOAD_DIR) {
    $name = $_GET["name"] ?? "";
    $target = realpath($UPLOAD_DIR . "/" . $name);
    $base = realpath($UPLOAD_DIR);
    if ($target === false || strpos($target, $base) !== 0) {
        return null;
    }
    return file_get_contents($target);
}

function importXml() {
    $body = file_get_contents("php://input");
    $xml = simplexml_load_string($body, "SimpleXMLElement", LIBXML_NOENT);
    return $xml;
}

function importXmlSafe() {
    $body = file_get_contents("php://input");
    $xml = simplexml_load_string($body);
    return $xml;
}

function registerWeak() {
    $password = $_POST["password"] ?? "";
    $hash = md5($password);
    return $hash;
}

function registerSafe() {
    $password = $_POST["password"] ?? "";
    $hash = password_hash($password, PASSWORD_DEFAULT);
    return $hash;
}

function startPasswordReset() {
    $token = rand(100000, 999999);
    return $token;
}

function startPasswordResetSafe() {
    $token = bin2hex(random_bytes(32));
    return $token;
}

function loginComplete() {
    $next = $_GET["next"] ?? "/";
    header("Location: " . $next);
}

function loginCompleteSafe() {
    $next = $_GET["next"] ?? "/";
    if (strpos($next, "/") !== 0 || strpos($next, "//") === 0) {
        $next = "/";
    }
    header("Location: " . $next);
}

?>
