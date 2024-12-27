<?php
include '../app/db/config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);
    $confirmPassword = mysqli_real_escape_string($conn, $_POST['confirm-password']);

    if ($password !== $confirmPassword) {
        die("Password dan konfirmasi password tidak cocok.");
    }

    $sql = "INSERT INTO user_register (username, email, password) VALUES ('$username', '$email', '$password')";
    if (mysqli_query($conn, $sql)) {
        echo "Registrasi berhasil!";
    } else {
        die("Query gagal: " . mysqli_error($conn));
    }
}
?>
