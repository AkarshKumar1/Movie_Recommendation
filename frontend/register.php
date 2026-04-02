<?php
$page = "register-page";   // controls background
include '../config.php';
include 'partials/header.php';

if (isset($_POST['register'])) {
    $username = $_POST['username'];
    $password = md5($_POST['password']);

    $conn->query("INSERT INTO users (username, password) VALUES ('$username', '$password')");
    echo "<script>alert('Registered successfully');</script>";
}
?>

<!-- REGISTER FORM -->
<div class="form-box">

    <h2>Register</h2>

    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button name="register">Register</button>
    </form>

</div>

<?php include 'partials/footer.php'; ?>