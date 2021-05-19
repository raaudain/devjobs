import React, { useState, useEffect } from "react";
import axios from "axios";
import Jobs from "./Jobs";
import Pagination from "./Pagination"

function Homepage() {
    const [jobs, setJobs] = useState([]);
    const [currPage, setCurrPage] = useState(1);
    const [jobsPerPage] = useState(20);

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

    // Divide jobs into pages
    const indexOfLastJob = currPage * jobsPerPage;
    const indexOfFirstJob = indexOfLastJob - jobsPerPage;
    const currJobs = jobs.slice(indexOfFirstJob, indexOfLastJob);


    return (
        <div className="container">
            <h1>Dev Jobs</h1>
            <div className="jobs-list">
                {currJobs.map((job, index) => 
                    <Jobs 
                        id={index} 
                        url={job.url}
                        title={job.title}
                        company={job.company}
                        timestamp={job.timestamp}
                        source={job.source}
                        sourceURL={job.source_url}
                        location={job.location}
                    />
                )}
            </div>
            <Pagination 
                jobsPerPage={jobsPerPage} 
                totalJobs={jobs.length}
                currPage={currPage}
                setCurrPage={setCurrPage}
            />
        </div>
    )
}

export default Homepage;