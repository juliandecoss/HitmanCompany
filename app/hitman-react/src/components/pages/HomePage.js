import React from 'react';
import {useState} from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function HomePage() {
    const persons = [{"job_id":1,"assigned_by":2,"assigned_to":2}, {"job_id":1,"assigned_by":2,"assigned_to":2}, {"job_id":1,"assigned_by":2,"assigned_to":2}];
    const [post, setPost] = useState({"hits":[]})
    React.useEffect(() => {
        const access_token = localStorage.getItem('accessToken');
        if(!access_token){
            window.location = "/"
        }
        const payload = { 'access_token':access_token}
        axios.post(
            'http://127.0.0.1:5000/hits', 
            payload,
            {
                headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
            },
        ).then((res) => {
            setPost(res.data)
            console.log(res.data.hits)
        })
    }, []);
    
    console.log("QUE TRAE EL POSTT: " + JSON.stringify(post))
    return (
        <div className="text-center">
            <h1 className="main-title home-page-title">Hitman Company</h1>
            <div class="table-wrapper">
                <table class="fl-table">
                    <thead>
                        <tr>
                        <th>Hits Id</th>
                        <th>Hitman Id</th>
                        <th>Manager Id</th>
                        </tr>
                    </thead>
                    <tbody>
                        {post.hits.map((val, key) => {
                        return (
                            <tr key={key}>
                            <Link to="/">
                                <td>{val.job_id}</td>
                            </Link>
                            <td>{val.assigned_to}</td>
                            <td>{val.assigned_by}</td>
                            </tr>
                        )
                        })}
                    </tbody>
                </table>
            </div>
            <Link to="/">
                <button className="primary-button">Log out</button>
            </Link>
        </div>
    )
}
