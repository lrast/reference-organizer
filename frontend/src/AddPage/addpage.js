import React, {useState, useEffect} from 'react'
import { FormControl, TextField, Button} from '@mui/material';

import {AutofillField} from '../myComponents'

function AddPage() {
  const [urlValue, setUrlValue] = useState("")

  const formFieldsDefaults = {url:"", name:"", topics:[]}
  const [formFields, setFormFields] = useState(formFieldsDefaults)

  useEffect( () => {
    if (urlValue != ""){
      fetch('api/getWebpageTitle', {method: 'POST', body: urlValue})
      .then((response)=>response.text())
      .then( (title) => { if (formFields.name==""){setFormFields( {...formFields, name: title } )} })
    }
  }, [urlValue])

  const inputStyling = {mb:"10pt", width:"80%"}

  return (
    <>
    <div style={{"textAlign":"center", "width":"100%", "cursor":"pointer"}}> 
      <h1> Add a new page </h1>
        <form
          onSubmit={(e)=> {
              e.preventDefault();
              fetch('/api/addentries', { method: 'POST', body: JSON.stringify( formFields )})
              setFormFields( formFieldsDefaults )
              setUrlValue("")
          } }
        >
          <FormControl sx={inputStyling} >
            <TextField 
            label="Page URL"
            value={formFields.url}
            inputProps = {{
              onBlur: (event) => {
                setUrlValue(event.target.value)
              },
              onChange: (event) => {
                setFormFields( {...formFields, url: event.target.value } )
              }
            }}>
            </TextField>
          </FormControl>
          <FormControl sx={inputStyling} >
            <TextField
              label="Page Name"
              value={formFields.name}
              inputProps = {{
                onChange: (event) => {
                  setFormFields( {...formFields, name: event.target.value } )
                }
              }}>
            </TextField>
          </FormControl>
          <FormControl sx={inputStyling} >
            <AutofillField toFetch="/api/topic/"
              autocompleteProps={{
              label:"Topics", multiple:true, freeSolo:true, autoSelect:true,
              value: formFields.topics,
              onChange: (event, newValue) => setFormFields( {...formFields, topics: newValue} )
            }}/>
          </FormControl>
          <FormControl sx={{mb:"10pt", width:"60%", height:"40pt"}} >
            <Button type="submit"
            variant="contained"
            style={{"cursor":"pointer"}}
            > Submit </Button>
          </FormControl>
        </form>
    </div>
    </>
  )
}

export default AddPage;
