<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

header('Content-Type: application/json');

$host = getenv('DB_HOST') ?: 'order-db';
$user = getenv('DB_USER') ?: 'order_user';
$password = getenv('DB_PASS') ?: 'order_pass';
$database = getenv('DB_NAME') ?: 'order_db';

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(["error" => "Database connection failed: " . $conn->connect_error]);
    exit();
}

$request_uri = strtok($_SERVER['REQUEST_URI'], '?');
$request_method = $_SERVER['REQUEST_METHOD'];

if ($request_uri === '/orders' && $request_method === 'GET') {
    $result = $conn->query("SELECT * FROM orders");
    if (!$result) {
        http_response_code(500);
        echo json_encode(["error" => "Failed to fetch orders: " . $conn->error]);
        exit();
    }
    $orders = [];
    while ($row = $result->fetch_assoc()) {
        $orders[] = $row;
    }
    echo json_encode(["orders" => $orders]);

} elseif ($request_uri === '/orders' && $request_method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);

    if (!isset($input['user_id'], $input['book_id'], $input['quantity'])) {
        http_response_code(400);
        echo json_encode(["error" => "Missing user_id, book_id, or quantity"]);
        exit();
    }

    $stmt = $conn->prepare("INSERT INTO orders (user_id, book_id, quantity) VALUES (?, ?, ?)");
    $stmt->bind_param("iii", $input['user_id'], $input['book_id'], $input['quantity']);
    if ($stmt->execute()) {
        echo json_encode(["message" => "Order created successfully", "order_id" => $stmt->insert_id]);
    } else {
        http_response_code(500);
        echo json_encode(["error" => "Failed to create order: " . $stmt->error]);
    }
    $stmt->close();

} elseif (preg_match('/^\/orders\/(\d+)$/', $request_uri, $matches) && $request_method === 'PUT') {
    $order_id = (int)$matches[1];
    $input = json_decode(file_get_contents('php://input'), true);

    if (!isset($input['user_id'], $input['book_id'], $input['quantity'])) {
        http_response_code(400);
        echo json_encode(["error" => "Missing user_id, book_id, or quantity"]);
        exit();
    }

    $stmt = $conn->prepare("UPDATE orders SET user_id = ?, book_id = ?, quantity = ? WHERE id = ?");
    $stmt->bind_param("iiii", $input['user_id'], $input['book_id'], $input['quantity'], $order_id);
    if ($stmt->execute()) {
        if ($stmt->affected_rows > 0) {
            echo json_encode(["message" => "Order updated successfully"]);
        } else {
            http_response_code(404);
            echo json_encode(["error" => "Order not found"]);
        }
    } else {
        http_response_code(500);
        echo json_encode(["error" => "Failed to update order: " . $stmt->error]);
    }
    $stmt->close();

} elseif (preg_match('/^\/orders\/(\d+)$/', $request_uri, $matches) && $request_method === 'DELETE') {
    $order_id = (int)$matches[1];

    $stmt = $conn->prepare("DELETE FROM orders WHERE id = ?");
    $stmt->bind_param("i", $order_id);
    if ($stmt->execute()) {
        if ($stmt->affected_rows > 0) {
            echo json_encode(["message" => "Order deleted successfully"]);
        } else {
            http_response_code(404);
            echo json_encode(["error" => "Order not found"]);
        }
    } else {
        http_response_code(500);
        echo json_encode(["error" => "Failed to delete order: " . $stmt->error]);
    }
    $stmt->close();

} else {
    http_response_code(404);
    echo json_encode(["error" => "Endpoint not found"]);
}

$conn->close();
?>
