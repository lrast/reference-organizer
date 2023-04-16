import React from 'react'

import { Link } from "react-router-dom";

function Home() {
    return (
        <>
          <h1>Welcome to organizer</h1>
          <h2> <Link to="/newpage"> Add Page </Link>  </h2>
          <h2> <Link to="/topic"> All Topics </Link>  </h2>
          <h2> <Link to="/page"> All Pages </Link>  </h2>
        </>
        )
}

export default Home;

