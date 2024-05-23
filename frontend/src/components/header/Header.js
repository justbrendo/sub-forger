
import React, { useState, useContext, useEffect } from 'react';
import { MdSubtitles } from "react-icons/md";
import "./Header.css"
function Header() {





    return (
        <div className='container-header'>
           
                <div className="logo">
                    <MdSubtitles ></MdSubtitles> TAB
                </div>
          

            <div className='subtext'>
                Com o Transcribe and Burn (TAB) é possivel
                trancrever legendas em videos de forma automática
                com ajuda de um módelo de IA.
            </div>
        </div>
    );
}

export default Header;