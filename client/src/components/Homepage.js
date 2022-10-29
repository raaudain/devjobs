import React, { useState, useEffect } from "react";
import { fetchData } from "./api";
import Pagination from "./Pagination";

function Homepage() {
    const [data, setData] = useState([])

    useEffect(async () => {
        const response = await fetchData();
        console.log(typeof(response))
        setData(response);
      }, []);

    console.log("hey", data[0])

    return (
        <div className="container">
            <Pagination data={data} />
            {data.map(i => (
                <div>
                    {i.url}
                </div>
            ))}
        </div>
    )
}

export default Homepage;