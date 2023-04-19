import React, {useState, useEffect} from 'react'
import {Sidebar, DataTable} from '../TableComponents'


function TopicsList() {
  const [tableData, setData] = useState(null);

  console.log('here')
  useEffect( () =>{
    fetch( '/api/topic')
    .then( (response) => console.log(response.json()) )
  })

  return (
      <div className="table-wrapper">
          <DataTable/>
          <Sidebar/>
      </div>
)
}

export default TopicsList;
