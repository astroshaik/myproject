import React, { Component } from "react";
import { render } from "react-dom";
import "./LoginStyle.css"; // Make sure the CSS file is in the same directory or adjust the path accordingly

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="login-form">
        <h2>Login</h2>
        <form id="loginForm">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="Enter your email"
            required
          />

          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Enter your password"
            required
          />

          <button type="submit">Log In</button>
        </form>
        <div className="register-link">
          <p>
            Don't have an account? <a href="#">Register here.</a>
          </p>
        </div>
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
