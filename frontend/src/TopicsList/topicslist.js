import React, {useState, useEffect} from 'react'
import {Sidebar, TableBody} from '../TableComponents'


function TopicsList() {
  const [tableData, setData] = useState([]);
  const [tableColumns, setColumns] = useState([]);

  useEffect( () => {
    fetch( '/api/topic/')
    .then( (response) => response.json())
    .then( (rawList) => rawList.map( (row) => 
          { return {'link': <a href={'/topic/' + row.id}> {row.name} </a> } }
        ))
    .then( (tableData) => {
          setData(tableData);
          setColumns( [{ Header: 'Topics', accessor: 'link'}] )
        })
  }, [])


  return (
      <div className="table-wrapper">
          <TableBody data={tableData} columns={tableColumns}/>
          <Sidebar/>
      </div>
)
}

export default TopicsList;
