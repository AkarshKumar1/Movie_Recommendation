<?php
session_start();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Movie Recommendation</title>

    <!-- CSS -->
    <link rel="stylesheet" href="/movie_recommendation/frontend/css/style.css">

    <!-- JS -->
    <script src="/movie_recommendation/frontend/js/script.js"></script>
</head>

<body class="<?php echo $page ?? ''; ?>">

<div class="container">

<div class="header">
    <h1>🎬 Movie Recommender</h1>

    <?php if (isset($_SESSION['user'])) { ?>
        <div class="logout">
           <a href="logout.php" class="logout-btn">Logout</a>
        </div>
    <?php } ?>
</div>

<hr>