import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 

function App() {
    const [url, setUrl] = useState('');
    const [response, setResponse] = useState('');
    const [error, setError] = useState('');
    
    const [loading, setLoading] = useState(false); 
    const [showResult, setShowResult] = useState(false); 

    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse('');
        setError('');
        setLoading(true);
        setShowResult(false);

        try {
            const res = await axios.post('http://localhost:8000/api/prompt', { url });
            setResponse(res.data.response);
            setShowResult(true);

        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred.');
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <div className="App">
            <h1>The Onboarder</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter URL"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Loading...' : 'Submit'}
                </button>
            </form>
            {response && (
                <div className={`result-container ${showResult ? 'visible' : ''}`}>
                    <img
                        src={response}
                        alt="Generated Result"
                        style={{ maxWidth: '100%', marginTop: '20px' }}
                    />
                </div>
            )}
            {error && <div><h2>Error:</h2><p>{error}</p></div>}
        </div>
    );
}

export default App;
