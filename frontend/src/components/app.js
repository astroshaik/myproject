import React, { Component } from 'react';
import { render } from 'react-dom';

// Define the App component that manages the state for the login form.
export default class App extends Component {
    constructor(props) {
        super(props);
        // Initialize the state with default values for email, password, and redirection flag.
        this.state = {
            email: '',
            password: '',
            redirectToRegistration: false // Controls whether to redirect the user to the registration page.
        };
    }

    // Event handler for form inputs. Updates state based on input changes.
    handleInputChange = (event) => {
        const { name, value } = event.target; // Destructure the name and value from event target.
        this.setState({ [name]: value }); // Dynamically update the state for the given input name.
    }

    // Handle form submission.
    handleSubmit = (event) => {
        event.preventDefault(); // Prevent default form submission behavior.
        // Log the email and password to the console. In a real app, you'd likely make a network request here.
        console.log('Login Submitted:', this.state.email, this.state.password);
        
        // Example conditional logic based on authentication result.
        // Uncomment and modify according to your authentication logic:
        // if credentials are incorrect, suggest redirection to the registration page
        // this.setState({ redirectToRegistration: true });
    }

    // Render method for displaying the component.
    render() {
        // Conditional rendering based on the redirectToRegistration state.
        if (this.state.redirectToRegistration) {
            // Log redirection to the console for demonstration.
            console.log("Redirect to registration page");
            // In a real scenario, use react-router-dom or similar library for navigation:
            // return <Redirect to="/register" />
        }

        // The login form JSX.
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
                        required  // Ensures that the email input is filled.
                    />
                </label>
                <label>
                    Password:
                    <input 
                        type="password" 
                        name="password" 
                        value={this.state.password} 
                        onChange={this.handleInputChange} 
                        required  // Ensures that the password input is filled.
                    />
                </label>
                <button type="submit">Login</button>
            </form>
        );
    }
}

// Identify the div element where the React app will be mounted.
const appDiv = document.getElementById('app');
// Render the App component into the identified div element.
render(<App />, appDiv);
