import React, {useState, useEffect} from 'react'
import {Sidebar, TableBody} from '../TableComponents'


function PagesList() {
  const [tableData, setData] = useState([]);
  const [tableColumns, setColumns] = useState([]);

  useEffect( () => {
    fetch( '/api/page/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (rawList) => rawList.map( (row) => 
          { return {'link': <a href={'/page/' + row.id}> {row.name} </a> } }
        ))
    .then( (tableData) => {
          setData(tableData);
          setColumns( [{ Header: 'Pages', accessor: 'link'}] )
        })
  }, [])


  return (
      <div className="table-wrapper">
          <TableBody data={tableData} columns={tableColumns}/>
          <Sidebar/>
      </div>
)
}

export default PagesList;
