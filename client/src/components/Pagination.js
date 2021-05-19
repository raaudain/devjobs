import React from 'react'

function Pagination({ jobsPerPage, totalJobs, setCurrPage, currPage }){
    const pageNumbers = [];
    const pages = Math.ceil(totalJobs / jobsPerPage);
    let index = 1;


    while (index <= pages) {
        pageNumbers.push(index);
        index++;
    }

    function paginate(pageNumber) {
        return setCurrPage(pageNumber);
    }

    function next() {
        return setCurrPage(currPage+1)
    }

    return (
        <div>
            <button>PREV</button>
            {pageNumbers.map(number => 
                <a href="!#" key={number}>
                    <span onClick={() => paginate(number)}>{number}</span>
                </a>
            )}
            <button onClick={() => next}>NEXT</button>
        </div>
    )
} 

export default Pagination;