import React, {useState, useEffect} from 'react'
import { FormControl, TextField, Button, Autocomplete } from '@mui/material';

import {AutofillField} from '../myComponents'

function AddPage() {
  const [urlValue, setUrlValue] = useState("")
  const [nameField, setNameField] = useState("")
  const [topicField, setTopicField] = useState([])

  useEffect( () =>{
    if (urlValue != ""){
      fetch('api/getWebpageTitle',
        {method: 'POST',
         body: urlValue}
       )
      .then((x)=>x.text())
      .then( (response) => {
        if (nameField==""){setNameField(response)}
      })
    }
  }, [urlValue])

  const inputStyling = {mb:"10pt", width:"80%"}


  return (
    <>
    <div style={{"textAlign":"center", "width":"100%"}}>
      <h1> Add a new page </h1>
        <form onSubmit={()=>
          fetch('/api/addentries', {
            method: 'POST',
            body: JSON.stringify({
              url: urlValue,
              name: nameField,
              topics: topicField
            })
          }) }
        >
          <FormControl sx={inputStyling} >
            <TextField 
            label="Page URL"
            inputProps = {{
              onBlur: (event) => {
                setUrlValue(event.target.value)
              }
            }}>
            </TextField>
          </FormControl>
          <FormControl sx={inputStyling} >
            <TextField
              label="Page Name"
              inputProps = {{
                onChange: (event) => {
                  setNameField( event.target.value )
                }
              }}
              id="nameField"
              value={nameField}>
            </TextField>
          </FormControl>
          <FormControl sx={inputStyling} >
            <AutofillField toFetch="/api/topic"
              autocompleteProps={{
              label:"Topics", multiple:true, freeSolo:true, autoSelect:true,
              value: topicField, onChange: (event, newValue) => { setTopicField(newValue) },
              onBlur: () => console.log( topicField)
            }}/>
          </FormControl>
          <FormControl sx={{mb:"10pt", width:"60%", height:"40pt"}} >
            <Button type="submit"> Submit </Button>
          </FormControl>
        </form>
    </div>
    </>
  )
}

export default AddPage;
