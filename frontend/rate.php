<?php
include '../config.php';
session_start();

$user = $_SESSION['user'];
$movie_id = $_POST['movie_id'];
$rating = $_POST['rating'];

$res = $conn->query("SELECT user_id FROM users WHERE username='$user'");
$row = $res->fetch_assoc();
$user_id = $row['user_id'];

// Prevent duplicate rating
$check = $conn->query("SELECT * FROM ratings WHERE user_id=$user_id AND movie_id=$movie_id");

if ($check->num_rows > 0) {
    $conn->query("UPDATE ratings SET rating=$rating WHERE user_id=$user_id AND movie_id=$movie_id");
} else {
    $conn->query("INSERT INTO ratings (user_id, movie_id, rating) VALUES ($user_id, $movie_id, $rating)");
}

header("Location: dashboard.php");
?>