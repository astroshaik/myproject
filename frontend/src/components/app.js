import React, { Component } from 'react';
import { render } from 'react-dom';

export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            password: '',
            redirectToRegistration: false // This will handle redirection to the registration page
        };
    }

    handleInputChange = (event) => {
        const { name, value } = event.target;
        this.setState({ [name]: value });
    }

    handleSubmit = (event) => {
        event.preventDefault();
        // Here you would typically check credentials against a backend.
        // For now, let's just log them to console.
        console.log('Login Submitted:', this.state.email, this.state.password);
        
        // If credentials are incorrect, set redirectToRegistration to true
        // this.setState({ redirectToRegistration: true });

        // In a real scenario, after backend validation, redirect to a different page or show error
    }

    render() {
        if (this.state.redirectToRegistration) {
            // This is where you'd use something like `react-router-dom` to redirect
            // return <Redirect to="/register" />
            console.log("Redirect to registration page");
        }

        return (
            <form onSubmit={this.handleSubmit}>
                <h1>Login</h1>
                <label>
                    Email:
                    <input 
                        type="email" 
                        name="email" 
                        value={this.state.email} 
                        onChange={this.handleInputChange} 
                        required 
                    />
                </label>
                <label>
                    Password:
                    <input 
                        type="password" 
                        name="password" 
                        value={this.state.password} 
                        onChange={this.handleInputChange} 
                        required 
                    />
                </label>
                <button type="submit">Login</button>
            </form>
        );
    }
}

const appDiv = document.getElementById('app');
render(<App />, appDiv);
