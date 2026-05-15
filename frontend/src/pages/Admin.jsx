import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

export default function Admin() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [activities, setActivities] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await axios.post(`${API_BASE}/admin/login`, { username, password });
      setLoggedIn(true);
      fetchActivity();
      fetchUsers();
    } catch {
      setError("Invalid username or password");
    }
  };

  const fetchActivity = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/admin/activity`, {
        params: { username, password },
      });
      setActivities(res.data);
    } catch {
      setError("Failed to load activity data");
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await axios.get(`${API_BASE}/admin/users`, {
        params: { username, password },
      });
      setUsers(res.data);
    } catch {
      // ignore
    }
  };

  useEffect(() => {
    if (loggedIn) {
      const interval = setInterval(fetchActivity, 30000);
      return () => clearInterval(interval);
    }
  }, [loggedIn]);

  if (!loggedIn) {
    return (
      <div className="admin-login-wrapper">
        <form className="admin-login-form" onSubmit={handleLogin}>
          <h2>🔒 Admin Login</h2>
          <p className="admin-subtitle">Enter credentials to access the dashboard</p>
          {error && <div className="admin-error">{error}</div>}
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />
          <button type="submit">Login</button>
        </form>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h2>📊 Admin Dashboard</h2>
        <button className="admin-logout" onClick={() => { setLoggedIn(false); setUsername(""); setPassword(""); }}>
          Logout
        </button>
      </div>

      <div className="admin-stats">
        <div className="admin-stat-card">
          <span className="admin-stat-num">{activities.length}</span>
          <span className="admin-stat-label">Total Activities</span>
        </div>
        <div className="admin-stat-card">
          <span className="admin-stat-num">
            {new Set(activities.map((a) => a.ip)).size}
          </span>
          <span className="admin-stat-label">Unique IPs</span>
        </div>
        <div className="admin-stat-card">
          <span className="admin-stat-num">
            {activities.filter((a) => {
              const t = new Date(a.timestamp);
              const now = new Date();
              return now - t < 24 * 60 * 60 * 1000;
            }).length}
          </span>
          <span className="admin-stat-label">Last 24h</span>
        </div>
      </div>

      {loading && <p className="admin-loading">Loading...</p>}

      {/* User Last Login Section */}
      <div className="admin-table-wrapper" style={{ marginBottom: "1.5rem" }}>
        <h3 style={{ padding: "1rem 1rem 0.5rem", color: "#a78bfa", margin: 0 }}>👥 App Users - Last Login</h3>
        <table className="admin-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Last Login</th>
              <th>IP</th>
              <th>Browser</th>
            </tr>
          </thead>
          <tbody>
            {users.length === 0 ? (
              <tr>
                <td colSpan="4" className="admin-empty">No user logins yet</td>
              </tr>
            ) : (
              users.map((u) => (
                <tr key={u.username}>
                  <td><strong>{u.username}</strong></td>
                  <td className="admin-mono">{u.last_login ? new Date(u.last_login).toLocaleString() : "Never"}</td>
                  <td className="admin-mono">{u.ip || "-"}</td>
                  <td className="admin-ua">{(u.user_agent || "").slice(0, 50)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="admin-table-wrapper">
        <table className="admin-table">
          <thead>
            <tr>
              <th>#</th>
              <th>User</th>
              <th>Action</th>
              <th>Detail</th>
              <th>IP</th>
              <th>Browser</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {activities.length === 0 ? (
              <tr>
                <td colSpan="7" className="admin-empty">No activity recorded yet</td>
              </tr>
            ) : (
              activities.map((a, i) => (
                <tr key={a.id}>
                  <td>{i + 1}</td>
                  <td><strong>{a.username || "-"}</strong></td>
                  <td><span className="admin-action-badge">{a.action}</span></td>
                  <td>{a.detail}</td>
                  <td className="admin-mono">{a.ip}</td>
                  <td className="admin-ua">{a.user_agent.slice(0, 50)}</td>
                  <td className="admin-mono">{new Date(a.timestamp).toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <button className="admin-refresh" onClick={() => { fetchActivity(); fetchUsers(); }}>🔄 Refresh</button>
    </div>
  );
}
