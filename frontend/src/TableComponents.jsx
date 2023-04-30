import React, {useState, useEffect, useRef} from 'react';

import {useTable} from 'react-table'

import {AutofillField} from './myComponents'

import {TextField, Button} from '@mui/material';

// table component
function TableBody({data, columns}) {
    data = React.useMemo( () => data, [data])
    columns = React.useMemo( () => columns, [columns] )

    const tableInstance = useTable({ columns, data })

    const {
      getTableProps,
      getTableBodyProps,
      headerGroups,
      rows,
      prepareRow,
    } = tableInstance


    return (
      <div className="table-body">
        <table {...getTableProps()} className="reference-table">
         <thead>
           {headerGroups.map(headerGroup => (
             <tr {...headerGroup.getHeaderGroupProps()}>
               {headerGroup.headers.map(column => (
                 <th {...column.getHeaderProps()}>
                   {column.render('Header')}
                 </th>
               ))}
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
function Sidebar() {
  const [tableFilters, setTableFilters] = useState([])
  const [allTopics, setTopics] = useState([])

  const stateRef = useRef()
  stateRef.current = tableFilters;

  const removeFilterByKey = (key) => {
    setTableFilters( stateRef.current.filter( (item) => (item.key != key) ) )
  }

  // load data and and relationships
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



  return (
    <div className="table-sidebar">
        <TextField type="text" name="test" label="Search" className="sidebar-filter-body" />
        <ul style={{listStyle: "none"}}>
          {tableFilters}
        </ul>
        <Button variant="contained" onClick={() => {
          setTableFilters( [...tableFilters,
            FilterComponent({myKey:(Math.max( ...tableFilters.map( (item) =>(item.key) ), 0 ) + 1 + ''),
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







class FilterList extends React.Component {
  // component representing the list of different filters
  constructor() {
    super()
    this.filters = [
        <SearchBar key="0" />,
        <li key="1">
          <a onClick={this.makeNewFilter.bind(this)} className="sidebar-filter-body">New Filter</a>
        </li>
      ]
    this.state = {filters: this.filters}
    this.totalNumberAdded = 2
  }

  makeNewFilter() {
    let key = this.totalNumberAdded += 1
    let newItem = FilterComponent(key, this)
    this.filters.splice(-1,0,newItem)
    this.setState( {filters: this.filters} )
  }

  removeFilter(key) {
    for (let i = 0; i<this.filters.length; i++){
      if (this.filters[i].key == key) {
        this.filters.splice(i, 1)
      }
    }
    this.setState( {filters: this.filters} )
  }

  render() {
    return React.createElement('ul',   {style: {listStyle: "none"}}, this.filters )
  }
}


function SearchBar(key) {
  return (
    <>
      <li className="sidebar-filter-item" key={key}>
        <div className="sidebar-filter-body">
            Search:
            <input type="text" name="test" style={{width: '30%'}} />
        </div>
      </li>
    </>
    )
}





export {TableBody, Sidebar };
