/* 
      main table element

*/


const divForTable = document.querySelector(".table-body")
const reactTableRoot = ReactDOM.createRoot( divForTable )


/*
var test2;
function update(data){
  test2 = data
}


const fetchTableData = async (path) => {
  const item = await fetch(`http://127.0.0.1:5000/api/${path}`);
  const items = await item.json()
  test2 = items
  // console.log(items)
  return items
}


const endpart = 'page'

const test = fetchTableData(endpart)
console.log( fetchTableData(endpart) )


const Table = () => {
  const [tableContent, setTableContent ] = React.useState([])
  React.useEffect(async() => {
    const items = await fetchTableData('page');
    setTableContent(items);


  }, []);
  return (
  <div>
  {tableContent?.map(item => <h1 key={item?.id}>{item?.title}</h1>)}
  </div>)
}

reactTableRoot.render(Table())
*/



/*  
      table sidebar:

*/
const sidebar = ReactDOM.createRoot( document.querySelector(".table-sidebar") )

class FilterList extends React.Component {
  // component representing the list of different filters
  constructor() {
    super()
    this.filters = [

        <li key="1">
          <a onClick={this.makeNewFilter.bind(this)} className="sidebar-filter-body">New Filter</a>
        </li>
      ]
    this.totalNumberAdded = 1
    this.makeNewFilter()
  }

  makeNewFilter() {
    // make a new Filter, add it to the list, rerender the list of filters
    let key = this.totalNumberAdded += 1
    let newItem = FilterComponent(key, this)
    this.filters.unshift(newItem)
    this.renderToSidebar()
  }

  removeFilter(key) {
    for (let i = 0; i<this.filters.length; i++){
      if (this.filters[i].key == key) {
        this.filters.splice(i, 1)
      }
    }

    this.renderToSidebar()
  }

  renderToSidebar() {
    sidebar.render( React.createElement('ul', null, this.filters ) )
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

currentFilters = new FilterList
currentFilters.renderToSidebar()









