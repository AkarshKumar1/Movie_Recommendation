<?php
$page = "login-page";   // controls background
include '../config.php';
include 'partials/header.php';

if (isset($_POST['login'])) {
    $username = $_POST['username'];
    $password = md5($_POST['password']);

    $result = $conn->query("SELECT * FROM users WHERE username='$username' AND password='$password'");

    if ($result->num_rows > 0) {
        $_SESSION['user'] = $username;
        header("Location: dashboard.php");
        exit();
    } else {
        echo "<script>alert('Invalid login');</script>";
    }
}
?>

<!-- LOGIN FORM -->
<div class="form-box">
    <h2>Login</h2>

    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button name="login">Login</button>
    </form>
</div>

<?php include 'partials/footer.php'; ?>