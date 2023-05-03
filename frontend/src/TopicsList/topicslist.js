import React, {useState, useEffect, useRef, useMemo} from 'react'
import {Sidebar, TableBody} from '../TableComponents'

import {matchSorter} from 'match-sorter'


function TopicsList() {
  const [tableData, setData] = useState([]);
  const [tableColumns, setColumns] = useState([]);

  const [searchString, setSearchString] = useState('')

  const columns = [
    { Header: 'Topics', 
      accessor: 'link',
      Cell: ({row: {original: {id, name } } }) => <a href={'/topic/' + id}> {name} </a>,
    },
    {
      Header: 'name',
      accessor: 'name',
      id: 'name',
      //Filter: () => {},
      //filter: (rows, id, filterValue) => {console.log('rows', rows[0]['original']); 
      //return matchSorter(rows, filterValue, { keys: ['original.name'] })}
    },
    {
      Header: 'id',
      accessor: 'id',
      id: 'id'
    }
  ]

  const hiddenColumns = ['name', 'id']

  useEffect( () => {
    fetch( '/api/topic/')
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
          searchString={searchString} hiddenColumns={hiddenColumns} />
          <Sidebar searchString={searchString} setSearchString={setSearchString}/>
      </div>
)
}

export default TopicsList;
