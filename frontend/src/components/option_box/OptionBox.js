
import React, { useState, useContext, useEffect } from 'react';
import { MdSubtitles } from "react-icons/md";
import LocalFileBox from './LocalFileBox';
import YTBox from './YTbox';
import "./Option.css"
function OptionBox() {
    const [selectedBox, setSelectedBox] = useState(null); 

    const showLocalFileBox = () => setSelectedBox('localFile');
    const showYTBox = () => setSelectedBox('yt');

    return (
        <div className='fullbox'>
            {selectedBox === null && (
                <>
                    <LocalFileBox onClick={() => setSelectedBox('localFile')} isSelected={false} goBack={() => setSelectedBox(null)} />
                    <YTBox onClick={() => setSelectedBox('yt')} isSelected={false} goBack={() => setSelectedBox(null)} />
                </>
            )}
            {selectedBox === 'localFile' && <LocalFileBox isSelected={true} goBack={() => setSelectedBox(null)}  />}
            {selectedBox === 'yt' && <YTBox isSelected={true}  goBack={() => setSelectedBox(null)} />}
        </div>
    );
}


export default OptionBox;