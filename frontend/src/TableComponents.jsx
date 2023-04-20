import React, {useState, useEffect} from 'react';

import {useTable} from 'react-table'

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
  return (
    <div className="table-sidebar">
        <FilterList/>
    </div>
    )
}



class FilterList extends React.Component {
  // component representing the list of different filters
  constructor() {
    super()
    this.filters = [
        <li key="1">
          <a onClick={this.makeNewFilter.bind(this)} className="sidebar-filter-body">New Filter</a>
        </li>
      ]
    this.state = {filters: this.filters}
    this.totalNumberAdded = 1
    this.makeNewFilter()
  }

  makeNewFilter() {
    // make a new Filter, add it to the list, rerender the list of filters
    let key = this.totalNumberAdded += 1
    let newItem = FilterComponent(key, this)
    this.filters.unshift(newItem)
    this.setState( {filters: this.filters} )
    //this.render()
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

function FilterComponent(key, parent) {
  // sets up blank filter element
  return <li className="sidebar-filter-item" key={key}>
    <div className="sidebar-filter-body">
      <div className="sidebar-filter-exit">
          <a onClick={() => parent.removeFilter.bind(parent)(key)}> X </a>
      </div>

      <form action="">
        <label htmlFor="filter-on"> On: </label>
        <select id="filter-on">
          <option > Name </option>
          <option > Relationship </option>
        </select>
        <input type="text" name="test" style={{width: '30%'}} />
      </form>
    </div>
  </li>
}

export {TableBody, Sidebar };
