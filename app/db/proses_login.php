<?php
$conn = new mysqli('localhost', 'root', '', 'manajemen_pengguna');

if ($conn->connect_error) {
    die("Koneksi gagal: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];

    $stmt = $conn->prepare("SELECT password_hash FROM user_register WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($password_hash);
        $stmt->fetch();

        if (password_verify($password, $password_hash)) {
            echo "Login berhasil! <a href='dashboard.html'>Masuk ke Dashboard</a>";
        } else {
            echo "Password salah.";
        }
    } else {
        echo "Email tidak ditemukan.";
    }

    $stmt->close();
}

$conn->close();
?>
