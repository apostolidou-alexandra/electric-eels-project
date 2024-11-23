import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [url, setUrl] = useState('');
    const [response, setResponse] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse('');
        setError('');

        try {
            const res = await axios.post('http://localhost:8000/api/prompt', { url });
            setResponse(res.data.response);
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred.');
        }
    };

    return (
        <div className="App">
            <h1>URL Prompt Processor</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter URL"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                />
                <button type="submit">Submit</button>
            </form>
            {response && <div><h2>Response:</h2><p>{response}</p></div>}
            {error && <div><h2>Error:</h2><p>{error}</p></div>}
        </div>
    );
}

export default App;
