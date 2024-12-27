<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require '../db/config.php';

$sql = "SELECT id, username, email FROM user_register";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="../app/css/style.dashboard.css">
</head>
<body>
    <div class="mp">
        <input type="text" placeholder="Username">
        <button>Dashboard</button>
        <button>Tambahkan Pengguna</button>
    </div>

    <div class="main">
        <h1>Dashboard</h1>
        <div class="actions">
            <button class="add">Tambah Pengguna</button>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nama Pengguna</th>
                    <th>Email</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>
                <?php
                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $row['id'] . "</td>";
                        echo "<td>" . $row['username'] . "</td>";
                        echo "<td>" . $row['email'] . "</td>";
                        echo "<td class='actions'>
                                <button class='edit'>Edit</button>
                                <button class='delete'>Hapus</button>
                              </td>";
                        echo "</tr>";
                    }
                } else {
                    echo "<tr><td colspan='4'>Tidak ada data pengguna</td></tr>";
                }
                ?>
            </tbody>
        </table>
    </div>
</body>
</html>

<?php
$conn->close();
?>
