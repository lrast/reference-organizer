import React, {useState, useEffect, useRef, useMemo} from 'react';

import {AutofillField} from './myComponents'
import {TextField, Button} from '@mui/material';

import {useTable, useFilters, useGlobalFilter} from 'react-table'
import {matchSorter} from 'match-sorter'



// table component
function TableBody({data, columns, filterValues, searchString, hiddenColumns=[]}) {
  data = useMemo( () => data, [data])
  columns = useMemo( () => columns, [columns] )

  const defaultColumn = React.useMemo(
    () => ({
      Filter: () => [],
    }),
    []
  )

  const instance = useTable({ columns, data, defaultColumn, 
      initialState: {hiddenColumns: hiddenColumns},
      globalFilter: (rows, id, filterValue) => matchSorter(rows, filterValue, { keys: ['original.name'] })
      },
      useFilters, useGlobalFilter)

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    setFilter,
    setAllFilters,
    state,
    setGlobalFilter
  } = instance

  useEffect ( () => {
    setGlobalFilter(searchString)
  }, [searchString])


    return (
      <div className="table-body">
        <table {...getTableProps()} className="reference-table">
         <thead>
           {headerGroups.map(headerGroup => (
             <tr {...headerGroup.getHeaderGroupProps()}>
               {headerGroup.headers.map(column => {
                //console.log(column)
                return <th {...column.getHeaderProps()}> {column.render('Header')} </th>
               }
              )}
             </tr>
           ))}
         </thead>
         <tbody {...getTableBodyProps()}>
           {rows.map(row => {
             prepareRow(row)
             return (
               <tr {...row.getRowProps()} className="wide-column" >
                 {row.cells.map(cell => {
                   return (
                     <td{...cell.getCellProps()}>
                       {cell.render('Cell')}
                     </td>
                   )
                 })}
               </tr>
             )
           })}
         </tbody>
        </table>
      </div>
   )
}





// table sidebar
function Sidebar({searchString, setSearchString} ) {
  // In the future, we going to want the set the values of all filters in one state

  // state of the sidebar of filters
  const [tableOfFilters, setTableOfFilters] = useState([])

  const stateRef = useRef()
  stateRef.current = tableOfFilters;

  const removeFilterByKey = (key) => {
    setTableOfFilters( stateRef.current.filter( (item) => (item.key != key) ) )
  }

  // state containin data and relationships
  const [allTopics, setTopics] = useState([])

  useEffect( () => {
    fetch('/api/topic/')
    .then( (response) => response.json())
    .then( (options) => options.map( 
      (propertiesDict) => {
        propertiesDict['label'] = propertiesDict['name']
        return propertiesDict 
      } ) )
    .then( (options) => options.sort( (a,b) => (a.label.toLowerCase() > b.label.toLowerCase())-0.5 ) )
    .then( (options) => setTopics(options)  )
  }, [])

  // state of the filters themselves





  return (
    <div className="table-sidebar">
        <TextField type="text" name="test" label="Search" className="sidebar-filter-body"
          value={searchString}
          InputProps = {{
            onChange: (event) => {
              setSearchString( event.target.value )
            }
          }}
         />
        <ul style={{listStyle: "none"}}>
          {tableOfFilters}
        </ul>
        <Button variant="contained" onClick={() => {
          setTableOfFilters( [...tableOfFilters,
            FilterComponent({myKey:(Math.max( ...tableOfFilters.map( (item) =>(item.key) ), 0 ) + 1 + ''),
              removeByKey:removeFilterByKey, loadedTopics:allTopics}
              ) ] )
        }} > New Filter</Button>
    </div>
  )
}




function FilterComponent({myKey, removeByKey, loadedTopics}) {
  // sets up blank filter element

  return <li className="sidebar-filter-item" key={myKey}>
    <div className="sidebar-filter-body">
      <div className="sidebar-filter-exit">
          <a onClick={() => {removeByKey(myKey)} }> X </a>
      </div>

      <form action="">
        <label htmlFor="filter-on"> On: </label>
        <select id="filter-on">
          <option > Name </option>
          <option > Relationship </option>
        </select>
        <input type="text" name="test" style={{width: '30%'}} />
        <AutofillField preLoaded={loadedTopics}
              autocompleteProps={{
              label:"Filter in", multiple:true
        }}/>
      </form>
    </div>
  </li>
}






export {TableBody, Sidebar };
