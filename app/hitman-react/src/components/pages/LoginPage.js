import React from 'react'
import {useState} from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import '../../App.css'


export default function SignInPage() {
    const [password, createUser] = useState('')
    const [email, createEmail] = useState('')
    const onSubmit = async (e) => {
      e.preventDefault()
      const post = { 'email':email,'password': password }
      try {
        const res = await axios.post(
                                    'http://127.0.0.1:5000/login', 
                                    post,
                                    {
                                        headers: {
                                        'Content-Type': 'application/json',
                                        Accept: 'application/json',
                                    },
                                    },
                                )
        console.log(res.data)
        localStorage.setItem('accessToken', res.data.access_token);
        window.location = "/hits"
      } catch (e) {
        console.log(e)
        alert(e)
      }
    }
    return (
        <div className="text-center m-5-auto">
            <h2>Sign in and kill</h2>
            <form onSubmit={onSubmit}>
                <p>
                    <label>Username or email address</label><br/>
                    <input type="text" name="first_name" required onChange={(event) => {createEmail(event.target.value)}} value={email}/>
                </p>
                <p>
                    <label>Password</label>
                    <Link to="/forget-password"><label className="right-label">Forget password?</label></Link>
                    <br/>
                    <input type="password" name="password" required onChange={(event) => {createUser(event.target.value)}} value={password}/>
                </p>
                <p>
                    <button id="sub_btn" type="submit">Login</button> 
                </p>
            </form>
            <footer>
                <p>First time? <Link to="/register">Create an account</Link>.</p>
                <p><Link to="/">Back to Homepage</Link>.</p>
            </footer>
        </div>
    )
}
