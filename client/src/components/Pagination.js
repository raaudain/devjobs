import React from 'react'


function Pagination({ data }) {
    const itemsPerPage = 20;
    let currentPage = 1;
    let filteredData = []
    let jobs = []

    
    function renderLimit(jobsArray, jobsPerPage, currPage) {
        currPage--;
        
        let start = jobsPerPage * currPage;
        let end = start + jobsPerPage;
        let paginated = jobsArray.slice(start, end);
        
        console.log("pag",paginated)
        jobs = paginated;
    }

    console.log(jobs)
    
    // renderLimit(data, itemsPerPage, currentPage)

    // console.log("j", renderLimit())

    // Infinite Scroll
    window.addEventListener("scroll", () => {
        const {scrollHeight, scrollTop, clientHeight} = document.documentElement;

        if (!filteredData.length) {
            if (scrollTop + clientHeight > scrollHeight - 100) {
                currentPage++;
                setTimeout(renderLimit(data, itemsPerPage, currentPage), 2000);
            }
        }
        else {
            if (scrollTop + clientHeight > scrollHeight - 10) {
                currentPage++;
                setTimeout(renderLimit(filteredData, itemsPerPage, currentPage), 2000);
            }
        }
    });

    return (
        <></>
    )
}

export default Pagination;