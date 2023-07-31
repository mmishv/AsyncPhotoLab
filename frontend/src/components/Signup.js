import React, {useState} from 'react';
import axios from 'axios';
import '../styles/Login.css';


function Signup() {
    const [email, setEmail] = useState('');
    const [password1, setPassword1] = useState('');
    const [password2, setPassword2] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (password1 !== password2) {
            console.error('Passwords do not match');
            return;
        }

        try {
            const response = await axios.post('/register/', {
                email,
                password: password1,
                first_name: firstName,
                last_name: lastName,
            });

            localStorage.setItem('access_token', JSON.stringify(response.data));

            console.log(response.data);
            window.location.href = '/';
        } catch (error) {
            console.error(error.response.data);
        }
    };

    return (
        <div className="login-container">
            <form className="form" onSubmit={handleSubmit}>
                <label className="label">
                    Email:
                    <input className="input" type="email" value={email}
                           onChange={(event) => setEmail(event.target.value)} required/>
                </label>
                <br/>
                <label className="label">
                    Password:
                    <input className="input" type="password" value={password1}
                           onChange={(event) => setPassword1(event.target.value)} required/>
                </label>
                <br/>
                <label className="label">
                    Confirm Password:
                    <input className="input" type="password" value={password2}
                           onChange={(event) => setPassword2(event.target.value)} required/>
                </label>
                <br/>
                <label className="label">
                    First Name:
                    <input className="input" type="text" value={firstName}
                           onChange={(event) => setFirstName(event.target.value)} required/>
                </label>
                <br/>
                <label className="label">
                    Last Name:
                    <input className="input" type="text" value={lastName}
                           onChange={(event) => setLastName(event.target.value)} required/>
                </label>
                <br/>
                <button className="login-button" type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default Signup;
