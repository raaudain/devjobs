import React from 'react'

function Jobs({ url, title, company, timestamp, source, sourceURL, location }) {
    const date = new Date(timestamp * 1000);
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = date.getMonth();
    const day = date.getDate();
    
    return (
        <div className="job-item">
            <div className="job-date">
                <span className="job-month">{months[month]}</span>
                <span className="job-day">{day}</span>
            </div>
            <div className="job-description">
                <div>
                    <a href={url} target="_blank" rel="noopener noreferrer">
                        <span className="title">{title}</span>
                    </a>
                </div>
                <div className="bottom">
                    <span className="company">{company || company !== "None" ? `${company}` : ""}</span>
                    <span className="location">{location || location !== "None" ? `${location}` : "" }</span>
                    
                    <span className="source">
                        Source: <a href={sourceURL} target="_blank" rel="noopener noreferrer">{source}</a>
                    </span>
                </div>
            </div>
        </div>
    )
} 

export default Jobs;