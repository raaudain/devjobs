import React from 'react'

function Jobs({ url, title, company, timestamp, source, sourceURL, index }) {
    return (
        <div className="job-item" key={index}>
            <a href={url} target="_blank" rel="noopener noreferrer">
                <span className="title">{title}</span>
                <span className="company">{company}</span>
                <span className="date">{timestamp}</span>
                <a href={sourceURL} target="_blank" rel="noopener noreferrer">
                    <span className="source">{source}</span>
                </a>
            </a>
        </div>
    )
} 

export default Jobs;