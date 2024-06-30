import React, { useState, useEffect } from 'react';
import { Form, Button, InputGroup } from 'react-bootstrap';
import { FaYoutube } from "react-icons/fa";

function extractVideoName(path) {
    const startIndex = path.indexOf('/downloads/') + '/downloads/'.length;
    const endIndex = path.indexOf('/burned_video.mp4');

    if (startIndex !== -1 && endIndex !== -1) {
        return path.substring(startIndex, endIndex);
    } else {
        return null; // or handle error condition as needed
    }
}

function YTForm() {
    const [url, setUrl] = useState('https://www.youtube.com/watch?v=JDjhs9hF9f0');
    const [selectedLanguage, setSelectedLanguage] = useState('en');
    const [translateToEnglish, setTranslateToEnglish] = useState(false);
    const [selectedModel, setSelectedModel] = useState('tiny');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [videoUrl, setVideoUrl] = useState('');
    const [outputPath, setOutputPath] = useState('');

    useEffect(() => {
        if (outputPath) {
            fetchVideo(outputPath);
        }
    }, [outputPath]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');
        setVideoUrl('');

        const requestBody = {
            url,
            language_code: selectedLanguage,
            model_name: selectedModel
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/generate_commands/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();
            if (response.ok) {
                setSuccess(data.message);
                setOutputPath(extractVideoName(data.output_path));
            } else {
                setError(data.detail);
            }
        } catch (err) {
            setError('An error occurred while communicating with the server.');
        } finally {
            setLoading(false);
        }
    };

    const handleLanguageChange = (e) => {
        setSelectedLanguage(e.target.value);
    };

    const handleTranslateChange = (e) => {
        setTranslateToEnglish(e.target.checked);
    };

    const handleModelChange = (e) => {
        setSelectedModel(e.target.value);
    };

    const fetchVideo = async (path) => {
        try {
            const response = await fetch(`http://localhost:8000/downloads/${path}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const blob = await response.blob();
            const videoObjectUrl = URL.createObjectURL(blob);
            setVideoUrl(videoObjectUrl);
        } catch (error) {
            console.error('Error fetching video:', error);
        }
    };

    return (
        <div>
            <div style={{ display: "flex", justifyContent: "center" }}>
                {videoUrl && (
                    <video controls autoPlay style={{ maxWidth: "80%" }}>
                        <source src={videoUrl} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                )}
            </div>

            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formYoutubeUrl">
                    <Form.Label>YouTube URL</Form.Label>
                    <InputGroup>
                        <Form.Control
                            type="url"
                            placeholder="...."
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            required
                        />
                        <Button variant="primary" type="submit" disabled={loading}>
                            {loading ? 'Loading...' : 'Submit'}
                        </Button>
                    </InputGroup>
                    {error && <div style={{ color: 'red' }}>{error}</div>}
                    {success && <div style={{ color: 'green' }}>{success}</div>}
                </Form.Group>
                <Form.Group controlId="formLanguage">
                    <Form.Label>Select Language</Form.Label>
                    <Form.Control as="select" value={selectedLanguage} onChange={handleLanguageChange}>
                        <option value="">Select Language</option>
                        <option value="pt">Portuguese</option>
                        <option value="oj">Ojibwa</option>
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="formModel">
                    <Form.Label>Select Model</Form.Label>
                    <Form.Control as="select" value={selectedModel} onChange={handleModelChange}>
                        <option value="">Select Model</option>
                        <option value="tiny">tiny</option>
                        <option value="tiny.en">tiny.en</option>
                        <option value="base">base</option>
                        <option value="base.en">base.en</option>
                        <option value="small">small</option>
                        <option value="small.en">small.en</option>
                        <option value="medium">medium</option>
                        <option value="medium.en">medium.en</option>
                        <option value="large">large</option>
                        <option value="large-v1">large-v1</option>
                        <option value="large-v2">large-v2</option>
                        <option value="large-v3">large-v3</option>
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="formTranslate">
                    <Form.Check
                        type="checkbox"
                        label="Translate to English"
                        checked={translateToEnglish}
                        onChange={handleTranslateChange}
                    />
                </Form.Group>
            </Form>
        </div>
    );
}

function YTBox({ onClick, isSelected, goBack }) {
    if (isSelected) {
        return (
            <div className='YTBoxSelected'>
                <h3 style={{ marginTop: "1em" }}>Transcribe YouTube Videos</h3>
                <YTForm />
                <div onClick={goBack}>Go Back</div>
            </div>
        );
    }

    return (
        <div onClick={onClick} className='yt box'>
            <div className='title'>Download YouTube videos</div>
            <div className='icon-box'>
                <FaYoutube />
            </div>
        </div>
    );
}

export default YTBox;
