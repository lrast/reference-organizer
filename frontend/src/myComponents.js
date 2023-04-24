// General use components

import React from 'react'
import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';


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











export {EditPanel};


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
