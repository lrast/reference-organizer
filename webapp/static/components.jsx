/* table sidebar */
const sidebar = ReactDOM.createRoot( document.querySelector(".table-sidebar") )

class FilterList extends React.Component {
  constructor() {
    super()
    this.filters = [
        React.createElement('li', {key:1}, 
          React.createElement('a', {onClick: this.makeNewFilter.bind(this), className:"sidebar-filter-body"},
           'new Filter')
        )
      ]
  }

  makeNewFilter() {
    // make a new Filter, add it to the list, rerender the list of filters
    console.log('call')
    let key = this.filters.length + 1
    let newItem = FilterComponent(key, this)
    this.filters.unshift(newItem)
    this.renderToSidebar()
  }

  removeFilter(key) {
  }

  renderToSidebar() {
    sidebar.render( React.createElement('ul', null, this.filters ) )
    }
}

function FilterComponent(key, parent) {
  // sets up blank filter element
  console.log(key)
  return <li className="sidebar-filter-item" key={key}>
    <div className="sidebar-filter-body">
      <div className="sidebar-filter-exit">
          <a> X </a>
      </div>

      <form action="">
        <label htmlFor="filter-on"> On: </label>
        <select id="filter-on">
          <option > Name </option>
          <option > Relationship </option>
        </select>
      </form>
    </div>
  </li>
}





currentFilters = new FilterList
currentFilters.renderToSidebar()

