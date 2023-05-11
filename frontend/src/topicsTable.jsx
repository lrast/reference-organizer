import React, {useState, useEffect, useContext} from 'react'

import {Sidebar, TableBody} from './TableComponents'

import {TopicContext, TableType} from './DataContext'

function TopicsTable() {
  //  Table columns and data
  const tableData = useContext(TopicContext)

  const tableColumns = [
    { Header: 'Topics', 
      accessor: 'link',
      Cell: ({row: {original: {id, name } } }) => <a href={'/topic/' + id}> {name} </a>,
    },
    {
      Header: 'name',
      accessor: 'name',
      id: 'name',
    },
    {
      Header: 'id',
      accessor: 'id',
      id: 'id',
      Filter: () => {},
      filter: React.useCallback( (rows, id, filterValue) => {
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
        <TableType.Provider value="topics">
          <TableBody
            data={tableData} columns={tableColumns}
            searchString={searchString} allFilters={tableFilters}
            hiddenColumns={hiddenColumns}
          />
          <Sidebar
            searchString={searchString} setSearchString={setSearchString}
            setFilterValues={setTableFilters}
          />
        </TableType.Provider>
      </div>
)
}

export default TopicsTable;
