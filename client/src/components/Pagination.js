import React from 'react'

function Pagination({ jobsPerPage, totalJobs, paginate }){
    const pageNumbers = [];
    const pages = Math.ceil(totalJobs / jobsPerPage);
    let index = 1;

    while (index <= pages) {
        pageNumbers.push(index);
        index++;
    }

    console.log(pageNumbers, jobsPerPage, totalJobs)
    return (
        <div>
            {pageNumbers.map(number => 
                <a href="!#" key={number}>
                    <span onClick={()=>paginate(number)}>{number}</span>
                </a>
            )}
        </div>
    )
} 

export default Pagination;