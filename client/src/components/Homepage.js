import React, { useState, useEffect } from "react";
import axios from "axios";

function Homepage() {
    const [jobs, setJobs] = useState({});

    useEffect(() => {
        const url = "https://raw.githubusercontent.com/raaudain/devjobs/main/server/data/data.json";

        axios
          .get(url)
          .then(res => {
            const jobs = res.data;
            setJobs(jobs);
          })
          .catch(err => console.log(err.response));
      }, []);

    return (
        <div className="container">
            <h1>Dev Jobs</h1>
            <div className="jobs-list">
                {Object.values(jobs).map((job, index) => 
                    <div className="job-item" key={index}>
                        <a href={job.url} target="_blank" rel="noopener noreferrer">
                            <span id="title">{job.title}</span>
                            <span id="company">{job.company}</span>
                            <span id="date">{job.timestamp}</span>
                            <a href={job.source_url} target="_blank" rel="noopener noreferrer">
                                <span id="source">{job.source}</span>
                            </a>
                        </a>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Homepage;