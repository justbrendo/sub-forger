import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

function OptionsForm() {
    const [selectedLanguage, setSelectedLanguage] = useState('');
    const [translateToEnglish, setTranslateToEnglish] = useState(false);

    const handleLanguageChange = (e) => {
        setSelectedLanguage(e.target.value);
    };

    const handleTranslateChange = (e) => {
        setTranslateToEnglish(e.target.checked);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Selecione a linguagem:', selectedLanguage);
        console.log('Traduzir para o Ingles:', translateToEnglish);
    };

    return (
        <div className='fullbox'>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formLanguage">
                    <Form.Label>Select Language</Form.Label>
                    <Form.Control as="select" value={selectedLanguage} onChange={handleLanguageChange}>
                        <option value="">Selecione a linguagem</option>
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="formTranslate">
                    <Form.Check type="checkbox" label="Translate to English" checked={translateToEnglish} onChange={handleTranslateChange} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </div>
    );
}

export default OptionsForm;
