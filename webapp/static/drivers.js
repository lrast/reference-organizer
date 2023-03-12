// script elements to include on all pages


/* autofilling forms*/
var autofillForms = document.querySelectorAll(".autofill-form")

for (const pageForm of autofillForms) {
  let thisInput = pageForm.querySelector("input[class='autofill-box']")
  let thisButton = pageForm.querySelector("input[type='submit']")
  let thisData = pageForm.querySelector("datalist")

  thisButton.addEventListener('click', function (event) {
    for ( option of thisData.querySelectorAll('option') ){

      if (option.value == thisInput.value) {

        endpoint = pageForm.getAttribute('data-endpoint')
        requestkey = option.getAttribute('data-requestkey')
        requestvalue = option.getAttribute('data-requestvalue')

        requestbody = {}
        requestbody[requestkey] = requestvalue


        fetch(endpoint , {method: 'POST', body: JSON.stringify(requestbody) })
        location.reload()
      }
    }
  })
}



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
  return React.createElement('li', {key: key, className:"sidebar-filter-item"},
      React.createElement('div', {className:"sidebar-filter-body"}, [

        React.createElement('div', {className:"sidebar-filter-exit"}, [
           React.createElement('a', null, 'X'),
        ]),
       
        React.createElement('form', {action:""}, [
          React.createElement('label', {for:"filter-on"}, "On: " ),
          React.createElement('select', {id:"filter-on"}, [
            React.createElement('option',null, 'Name'),
            React.createElement('option',null, 'Relationship'),
          ])
        ])
        
      ])
   )
}





currentFilters = new FilterList
currentFilters.renderToSidebar()












/*
submitButton.addEventListener('click', makeText)
urlField.addEventListener('blur', deselectURL)



function deselectURL(event){
  if (nameField.value == "") {
    if (urlField.value==""){
      return
    }

    let resourceTitle = fetch("{{url_for('api.getWebpageTitle')}}",
      {method: 'POST',
       body: urlField.value}).then((x)=>x.text()).then( (title)=>nameField.value=title )
  }
}

function makeText(event) {
  topicField.type = "text"
  console.log(topicField.type)
}
*/

