import React, {useState, useEffect, useRef, useMemo} from 'react'
import {Sidebar, TableBody} from './TableComponents'

function TopicsTable() {
  //  Table columns and data
  const [tableData, setData] = useState([]);
  const [tableColumns, setColumns] = useState([]);

  const columns = [
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
        //console.log('in filter', filterValue, rows)
        if (filterValue.length == 0) { return rows}
        return rows.filter( (row) => ( filterValue.includes( row.original.id ) ) )
      }, [])
    }
  ]

  const hiddenColumns = ['name', 'id']

  // to do: use data that was passed to me
  useEffect( () => {
    fetch( '/api/topic/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (tableData) => {
          setData(tableData);
          setColumns( columns )
        })
  }, [])


  // Table filters
  const [searchString, setSearchString] = useState('')
  const [filtersFromSidebar, setFiltersFromSidebar] = useState( {topic: {in: [], out:[]}, page:{ in:[], out:[]} } )
  const [filtersToTable, setFiltersToTable] = useState([{id:"id", value:[]}])


  useEffect( () =>{
    // send filters from sidebar to table
    let includedTopics = tableData.map( (x) => x.id )
    if (filtersFromSidebar.topic.in.length != 0) { includedTopics = filtersFromSidebar.topic.in}
    includedTopics = includedTopics.filter( (x) => (! filtersFromSidebar.topic.out.includes(x) ) )

    console.log( 'parent effect', [{id:'id', value:includedTopics}] )
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
