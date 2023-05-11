import React, {useState, useEffect, useContext} from 'react'

import {Sidebar, TableBody} from './TableComponents'

import {PageContext, TableType} from './DataContext'

import {backendURL} from './config'

function PagesTable() {
  // table columns and data
  const tableData = useContext(PageContext)

  const tableColumns = [
    { Header: 'Pages', 
      accessor: 'link',
      Cell: ({row: {original: {id, name } } }) => <a href={backendURL +'/openpage/' + id}> {name} </a>
    },
    {
      id: 'info',
      Cell: ({row: {original: {id, name } } }) => <a href={'/page/' + id}> info </a>
    },
    {
      Header: 'name',
      id: 'name',
    },
    {
      Header: 'id',
      id: 'id',
      Filter: () => {},
      filter: React.useCallback( (rows, id, filterValue) => {
        //console.log('in filter', filterValue )
        let toDisplay = rows
        if (filterValue.in != null) { 
          toDisplay = toDisplay.filter( (r) => filterValue.in.includes(r.original.id) ) 
        }
        if (filterValue.out != null) {
          toDisplay = toDisplay.filter( r => !filterValue.out.includes(r.original.id)  )
        }
        return toDisplay
      }, [])
    } 
  ]
  const hiddenColumns = ['name', 'id']


  // Table filters
  const [searchString, setSearchString] = useState('')
  const [tableFilters, setTableFilters] = useState( {in:null, out:null} )

  return (
      <div className="table-wrapper">
        <TableType.Provider value="pages">
          <TableBody
            data={tableData} columns={tableColumns} 
            searchString={searchString} allFilters={tableFilters}
            hiddenColumns={hiddenColumns}
          />
          <Sidebar
            searchString={searchString} setSearchString={setSearchString} setFilterValues={setTableFilters}
          />
        </TableType.Provider>
      </div>
)
}

export default PagesTable;
