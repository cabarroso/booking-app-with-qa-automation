import { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await API.post("/auth/login", {
                username,
                password
            });

            localStorage.setItem("token", response.data.token);

            navigate("/bookings");
        } catch (err) {
            setError("Invalid credentials");
        }
    };


    return (
        <div>
            <h2>Login</h2>

            <input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />

            <input
              id="password"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={handleLogin}>Login</button>

            {error && <p className="error-message">{error}</p>}
        </div>
    );
}

export default Login;