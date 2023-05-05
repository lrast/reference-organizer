import React, {useState, useEffect} from 'react'
import {Sidebar, TableBody} from './TableComponents'

function PagesTable() {
  // table columns and data
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
      id: 'id',
      Filter: () => {},
      filter: (rows, id, filterValue) => {console.log('call'); 
      return rows }
    } 
  ]

  const [tableData, setData] = useState([]);
  const [tableColumns, setColumns] = useState([]);

  const hiddenColumns = ['name', 'id']

  // to do: use data that was passed to me
  useEffect( () => {
    fetch( '/api/page/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (tableData) => {
          setData(tableData);
          setColumns( columns )
        })
  }, [])



  // table filters
  const [searchString, setSearchString] = useState('')
  const [filtersFromSidebar, setFiltersFromSidebar] = useState([])
  const [filtersToTable, setFiltersToTable] = useState([])


  useEffect( () =>{
    // send filters from sidebar to table
    console.log(filtersFromSidebar)
  }, [filtersFromSidebar])



  return (
      <div className="table-wrapper">
          <TableBody
            data={tableData} columns={tableColumns} 
            searchString={searchString} allFilters={filtersToTable}
            hiddenColumns={hiddenColumns}
          />
          <Sidebar
            searchString={searchString} setSearchString={setSearchString}
            filterValues={filtersFromSidebar} setFilterValues={setFiltersFromSidebar}
          />
      </div>
)
}

export default PagesTable;
