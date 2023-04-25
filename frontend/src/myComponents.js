// General use components

import React, {useState, useEffect} from 'react'
import { Accordion, AccordionSummary, AccordionDetails,
        Autocomplete, TextField, Chip} from '@mui/material';


function EditPanel ({rootType, rootId}){
  return (
    <>
    <Accordion>
      <AccordionSummary>
        Edit
      </AccordionSummary>
      <AccordionDetails>
        MORE from my components! {rootType}
      </AccordionDetails>
    </Accordion>
    </>
    )
}

function AutofillField( {toFetch, preLoaded, autocompleteProps} ){
  const [options, setOptions] = useState([])

  useEffect( () => {
    if (preLoaded){
      setOptions(preLoaded)
    }
    else {
      fetch( toFetch )
      .then( (response) => response.json())
      .then( (options) => options.map( 
        (propertiesDict) => {
          propertiesDict['label'] = propertiesDict['name']
          return propertiesDict 
        } ) )
      .then( (options) => options.sort( (a,b) => (a.label.toLowerCase() > b.label.toLowerCase())-0.5 ) )
      .then( (options) => setOptions(options)  )
    }
  }, [])

  return(
  <Autocomplete
    {...autocompleteProps}
    options={options}
    renderTags={(value, getTagProps) => 
      value.map((option, index) => {
        let chipLabel = option.label
        if (typeof(option) === 'string'){
          chipLabel = option
        }
        return <Chip variant="outlined" label={chipLabel} {...getTagProps({ index })} />
      }
      )
    }
    renderInput={(params) => <TextField multiple {...params} label={autocompleteProps.label} />} >
  </Autocomplete>
  )
}




export {EditPanel, AutofillField};


/* autofilling forms

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
*/



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

