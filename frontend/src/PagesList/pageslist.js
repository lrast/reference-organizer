import React, {useState, useEffect} from 'react'
import {Sidebar, TableBody} from '../TableComponents'


function PagesList() {
  const [tableData, setData] = useState([]);
  const [tableColumns, setColumns] = useState([]);

  const [searchString, setSearchString] = useState('')

  const columns = [
    { Header: 'Pages', 
      accessor: 'link',
      Cell: ({row: {original: {id, name } } }) => <a href={'/page/' + id}> {name} </a>
    },
    {
      Header: 'name',
      id: 'name',
    },
    {
      Header: 'id',
      id: 'id'
    }
  ]

  const hiddenColumns = ['name', 'id']


  useEffect( () => {
    fetch( '/api/page/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (tableData) => {
          setData(tableData);
          setColumns( columns )
        })
  }, [])


  return (
      <div className="table-wrapper">
          <TableBody data={tableData} columns={tableColumns} 
            searchString={searchString} hiddenColumns={hiddenColumns}/>
          <Sidebar searchString={searchString} setSearchString={setSearchString}/>
      </div>
)
}

export default PagesList;
