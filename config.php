<?php
$conn = new mysqli("localhost", "root", "", "movie_recommendation");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
