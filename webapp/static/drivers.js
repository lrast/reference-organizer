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
          React.createElement('a', {onClick: this.makeNewFilter.bind(this)}, 'new Filter')
        )
      ]
  }

  makeNewFilter() {
    // make a new Filter, add it to the list, rerender the list of filters
    let key = this.filters.length + 1
    console.log(key)
    let newItem = React.createElement('li', {key: key}, 'element '+ (key-1) )
    this.filters.unshift(newItem)
    this.renderToSidebar()
  }

  renderToSidebar() {
    sidebar.render( React.createElement('ul', null, this.filters ) )
    }
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

