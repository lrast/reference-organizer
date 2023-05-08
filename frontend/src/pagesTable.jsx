import React, {useState, useEffect, useContext} from 'react'

import {Sidebar, TableBody} from './TableComponents'

import {PageContext} from './DataContext'

function PagesTable() {
  // table columns and data
  const tableData = useContext(PageContext)

  const tableColumns = [
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
      filter: (rows, id, filterValue) => { 
      return rows }
    } 
  ]
  const hiddenColumns = ['name', 'id']


  // table filters
  const [searchString, setSearchString] = useState('')
  const [filtersFromSidebar, setFiltersFromSidebar] = useState([])
  const [filtersToTable, setFiltersToTable] = useState([])


  useEffect( () =>{
    // send filters from sidebar to table
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
