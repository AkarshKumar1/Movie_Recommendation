<?php
include '../config.php';
include 'partials/header.php';

if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit();
}

$user = $_SESSION['user'];

// Get user_id
$res = $conn->query("SELECT user_id FROM users WHERE username='$user'");
$row = $res->fetch_assoc();
$user_id = $row['user_id'];

// 🔥 TEMP TEST (Uncomment if needed)
// $user_id = 1;

$search = $_GET['search'] ?? '';

// Movie search
if ($search != '') {
    $result = $conn->query("SELECT * FROM movies WHERE title LIKE '%$search%' LIMIT 50");
} else {
    $result = $conn->query("SELECT * FROM movies LIMIT 50");
}

// 🔥 CALL FLASK API
$url = "https://movie-recommendation-api-mpsa.onrender.com/recommend?user_id=$user_id";

// Fetch data safely
$response = @file_get_contents($url);

if ($response === FALSE) {
    $recommended_movies = [];
} else {
    $recommended_movies = json_decode($response, true); // ✅ important fix
}
?>

<!-- SEARCH BOX -->
<div class="search-box">
    <form method="GET">
        <input type="text" name="search" placeholder="Search movies...">
        <button type="submit">Search</button>
    </form>
</div>

<!-- RECOMMENDATIONS -->
<h2>🎯 Recommended For You</h2>

<div class="recommend-box">
<?php
if (!empty($recommended_movies) && is_array($recommended_movies)) {
    foreach ($recommended_movies as $movie) {
        echo "<p>⭐ $movie</p>";
    }
} else {
    echo "<p>Rate some movies to get recommendations</p>";
}
?>
</div>

<!-- MOVIES -->
<h2>🎥 Movies</h2>

<div class="grid">
<?php while ($row = $result->fetch_assoc()) { ?>
    <div class="movie-card">
        <h3><?php echo $row['title']; ?></h3>
        <p><?php echo $row['genres']; ?></p>

        <form action="rate.php" method="POST" class="rating-box">
            <input type="hidden" name="movie_id" value="<?php echo $row['movie_id']; ?>">
            <input type="number" name="rating" min="1" max="5" required>
            <button type="submit">⭐ Rate</button>
        </form>
    </div>
<?php } ?>
</div>

<?php include 'partials/footer.php'; ?>
<?php } ?>
</div>

<?php include 'partials/footer.php'; ?>
