import React, { useState } from "react";

export default function Register() {
  const [form, setForm] = useState({ username: "", first_name: "", last_name: "", email: "", password: "" });
  const [message, setMessage] = useState("");

  function update(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function submit(event) {
    event.preventDefault();
    setMessage("");
    try {
      const response = await fetch("/api/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const result = await response.json();
      setMessage(result.message || result.error || "Registration completed.");
    } catch {
      setMessage("Unable to reach the server. Please try again.");
    }
  }

  return (
    <main className="register-page">
      <h1>Sign-up</h1>
      <form onSubmit={submit}>
        <label htmlFor="username">Username</label>
        <input id="username" name="username" value={form.username} onChange={update} required />
        <label htmlFor="first_name">First Name</label>
        <input id="first_name" name="first_name" value={form.first_name} onChange={update} required />
        <label htmlFor="last_name">Last Name</label>
        <input id="last_name" name="last_name" value={form.last_name} onChange={update} required />
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" value={form.email} onChange={update} required />
        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" value={form.password} onChange={update} required minLength={8} />
        <button type="submit" className="btn btn-success">Register</button>
      </form>
      <p role="status">{message}</p>
    </main>
  );
}
