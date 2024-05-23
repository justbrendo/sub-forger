
import React, { useState, useContext, useEffect } from 'react';

import "./Option.css"
import { FaYoutube } from "react-icons/fa";
import { Form, Button,InputGroup } from 'react-bootstrap';
function YTForm() {
    const [url, setUrl] = useState('');

    // call back end here
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('YouTube URL:', url);
    };

    const [selectedLanguage, setSelectedLanguage] = useState('');
    const [translateToEnglish, setTranslateToEnglish] = useState(false);

    const handleLanguageChange = (e) => {
        setSelectedLanguage(e.target.value);
    };

    const handleTranslateChange = (e) => {
        setTranslateToEnglish(e.target.checked);
    };

 

    return (
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
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </InputGroup>
               
                <Form.Group controlId="formLanguage">
                    <Form.Label>Select Language</Form.Label>
                    <Form.Control as="select" value={selectedLanguage} onChange={handleLanguageChange}>
                        <option value="">Selecione a linguagem</option>
                        <option value="pt">Portuguese</option>
                        <option value="pt"> Ojibwa</option>
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                        
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="formTranslate">
                    <Form.Check type="checkbox" label="Traduzir para ingles" checked={translateToEnglish} onChange={handleTranslateChange} />
                </Form.Group>
            </Form.Group>
        </Form>
    );
}
function YTBox({ onClick, isSelected, goBack }) {

    if (isSelected == true) {
        return (
           
                <div className='YTBoxSelected'>
                    <h3 style={{marginTop:"1em"}}>Transcreva Videos do YouTube</h3>
                    <YTForm />
                   
                    <div onClick={goBack}>
                             Voltar
                    </div>
                </div>
            );
    }



    return (
        <div onClick={onClick} className='yt box'>
            <div className='title'>
                Baixe videos do  youtube

            </div>
            <div className='icon-box'>
                <FaYoutube></FaYoutube>
            </div>
        </div>
    );
}

export default YTBox;