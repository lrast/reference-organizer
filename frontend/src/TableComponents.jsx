import React from 'react';
import { useState } from 'react';
import ReactDOM from 'react-dom/client';

// table component



//To do


// table sidebar
function Sidebar() {
  return (
    <div className="table-sidebar">
        <FilterList/>
    </div>
    )
}


export default Sidebar;


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
    console.log(this.filters)
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
    console.log(this.filters)
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

