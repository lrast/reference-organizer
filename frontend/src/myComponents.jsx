// General use components

import React, {useState, useEffect} from 'react'
import { useNavigate } from "react-router-dom";

import { Accordion, AccordionSummary, AccordionDetails,
        Autocomplete, TextField, Chip, Button} from '@mui/material';



function EditPanel ({parentType, parentData}){
  const [formState, setFormState] = useState({})

  useEffect( () => {
    setFormState({name:parentData.name, url:parentData.url})
  }, [parentData])

  let formFieldNames = [""]
  let endpoint = ""

  if (parentType ==  "page") {
    formFieldNames = ["url", "name"]
    endpoint = '/api/page/' + parentData.id
  }
  else if (parentType == "topic") {
    formFieldNames = ["name"]
    endpoint = '/api/topic/' + parentData.id
  }

  let redirect = useNavigate()

  return (
    <Accordion>
      <AccordionSummary>
        Edit {parentType}
      </AccordionSummary>
      <AccordionDetails>
        <form >
          { formFieldNames.map( (fieldName) => <TextField required label={fieldName} value={formState[fieldName]} sx={{width:'100%', mb:'10pt'}}
          InputProps = {{
            onChange: (event) => {
              setFormState( {...formState, [fieldName]: event.target.value } )
            }
          }}
          InputLabelProps = {{
            shrink:true
          }}
          />
          )}
          <Button type="submit" variant="contained" onClick={
            () => { fetch(endpoint, {method: 'PUT', body:JSON.stringify(formState) }) }
          }> Save edits </Button>
          <Button type="submit" variant="contained" color='error' sx={{float:'right'}} onClick={
            () => {fetch(endpoint, {method:'DELETE'}); redirect("/" + parentType)}
          }> Delete {parentType}</Button>
        </form>
      </AccordionDetails>
    </Accordion>
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




