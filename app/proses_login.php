<?php
include '../app/db/config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);

    $sql = "SELECT * FROM user_login WHERE email='$email' AND password='$password'";
    // $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) > 0) {
        header("Location: dashboard.php");
    } else {
        echo "Login gagal: Email atau password salah.";
    }
}
?>
