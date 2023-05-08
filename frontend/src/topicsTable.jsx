import React, {useState, useEffect, useRef, useMemo, useContext} from 'react'

import {Sidebar, TableBody, computeInclusionExclusion} from './TableComponents'

import {TopicContext} from './DataContext'

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
        if (filterValue.length == 0) { return rows}
        return rows.filter( (row) => ( filterValue.includes( row.original.id ) ) )
      }, [])
    }
  ]
  const hiddenColumns = ['name', 'id']



  // Table filters
  const [searchString, setSearchString] = useState('')
  const [filtersFromSidebar, setFiltersFromSidebar] = useState( {topic: {in: [], out:[]}, page:{ in:[], out:[]} } )
  const [filtersToTable, setFiltersToTable] = useState([{id:"id", value:[]}])


  useEffect( () =>{
    // collate the filters from sidebar and send them to table
    let includedTopics = tableData.map( (x) => x.id )
    if (filtersFromSidebar.topic.in.length != 0) { includedTopics = filtersFromSidebar.topic.in}

    includedTopics = includedTopics.filter( (x) => (! filtersFromSidebar.topic.out.includes(x) ) )


    setFiltersToTable( [{id:'id', value:includedTopics}] )
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
            setFilterValues={setFiltersFromSidebar}
          />
      </div>
)
}

export default TopicsTable;
