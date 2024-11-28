import React, {useState, useEffect} from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [orders, setOrders] = useState([]);
    const [users, setUsers] = useState([]);
    const [books, setBooks] = useState([]);
    const [newOrder, setNewOrder] = useState({user_id: "", book_id: "", quantity: 1});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [showOrders, setShowOrders] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [usersResponse, booksResponse] = await Promise.all([
                    axios.get("http://localhost:5000/users"),
                    axios.get("http://localhost:5001/catalog")
                ]);
                setUsers(usersResponse.data?.users || []);
                setBooks(booksResponse.data?.books || []);
            } catch (err) {
                setError("Error fetching users or books");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const fetchOrders = async () => {
        try {
            setLoading(true);
            const ordersResponse = await axios.get("http://localhost:5002/orders");
            console.log("Orders response:", ordersResponse.data);
            setOrders(ordersResponse.data.orders || []);
        } catch (err) {
            console.error("Error fetching orders:", err);
            setError("Error fetching orders");
        } finally {
            setLoading(false);
        }
    };

    const createOrder = () => {
        if (!newOrder.user_id || !newOrder.book_id || newOrder.quantity < 1) {
            setError("Please select a user, a book, and provide a valid quantity.");
            return;
        }
        setError("");
        setLoading(true);
        axios.post("http://localhost:5002/orders", newOrder)
            .then(() => {
                setNewOrder({user_id: "", book_id: "", quantity: 1});
                alert("Order created!");
                fetchOrders();
            })
            .catch((err) => {
                console.error("Error creating order:", err);
                setError("Error creating order");
            })
            .finally(() => setLoading(false));
    };

    return (
        <div className="app-container">
            <h1>Order Management</h1>
            {loading && <p className="loading">Loading...</p>}
            {error && <p className="error">{error}</p>}

            <button
                className="show-orders-button"
                onClick={() => {
                    fetchOrders();
                    setShowOrders(!showOrders);
                }}
            >
                {showOrders ? "Hide Orders" : "Show Orders"}
            </button>

            {showOrders && (
                <div className="orders-section">
                    <h2>Orders</h2>
                    <ul className="orders-list">
                        {orders.length > 0 ? (
                            orders.map((order) => (
                                <li key={order.id} className="order-item">
                                    <strong>Order ID:</strong> {order.id},
                                    <strong> User ID:</strong> {order.user_id},
                                    <strong> Book ID:</strong> {order.book_id},
                                    <strong> Quantity:</strong> {order.quantity},
                                    <strong> Created At:</strong> {order.created_at}
                                </li>
                            ))
                        ) : (
                            <p>No orders found.</p>
                        )}
                    </ul>
                </div>
            )}

            <div className="form-section">
                <h2>Create Order</h2>
                <label>
                    <span>Select User:</span>
                    <select
                        value={newOrder.user_id}
                        onChange={(e) => setNewOrder({...newOrder, user_id: e.target.value})}
                        className="dropdown"
                    >
                        <option value="">-- Select User --</option>
                        {users.map((user) => (
                            <option key={user.id} value={user.id}>
                                {user.name} ({user.email})
                            </option>
                        ))}
                    </select>
                </label>

                <label>
                    <span>Select Book:</span>
                    <select
                        value={newOrder.book_id}
                        onChange={(e) => setNewOrder({...newOrder, book_id: e.target.value})}
                        className="dropdown"
                    >
                        <option value="">-- Select Book --</option>
                        {books.map((book) => (
                            <option key={book.id} value={book.id}>
                                {book.title} by {book.author}
                            </option>
                        ))}
                    </select>
                </label>

                <label>
                    <span>Quantity:</span>
                    <input
                        type="number"
                        min="1"
                        value={newOrder.quantity}
                        onChange={(e) => setNewOrder({...newOrder, quantity: +e.target.value})}
                        className="input-field"
                    />
                </label>
                <button onClick={createOrder} className="create-order-button">Create Order</button>
            </div>
        </div>
    );
}

export default App;
