import React from 'react'

function Jobs({ url, title, company, timestamp, source, sourceURL, location }) {
    const date = new Date(timestamp * 1000).toLocaleString()

    return (
        <div className="job-item" id="">
                <div>
                    <span className="date">{date}</span>
                    <a href={url} target="_blank" rel="noopener noreferrer">
                        <span className="title">{title}</span>
                    </a>
                </div>
                <div>
                    <span className="company">{company || company === "None" ? `Company: ${company}` : null}</span>
                    <span className="location">{location || location === "None" ? `Location: ${location}` : null }</span>
                    <a href={sourceURL} target="_blank" rel="noopener noreferrer">
                        <span className="source">Source: {source}</span>
                    </a>
                </div>
        </div>
    )
} 

export default Jobs;