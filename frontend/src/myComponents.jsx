// General use components

import React, {useState, useEffect} from 'react'
import { useNavigate } from "react-router-dom";

import { Accordion, AccordionSummary, AccordionDetails,
        Autocomplete, TextField, Chip, Button, Card, CardContent} from '@mui/material';



function EditPanel ({parentType, parentData}){
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

  const [formState, setFormState] = useState({name:parentData.name, url:parentData.url})

  useEffect( () => {
    setFormState({name:parentData.name, url:parentData.url})
  }, [parentData])


  let redirect = useNavigate()

  return (
    <Accordion>
      <AccordionSummary>
        Edit {parentType}
      </AccordionSummary>
      <AccordionDetails>
        { formFieldNames.map( (fieldName) => 
          <TextField required sx={{width:'100%', mb:'10pt'}}
            label={fieldName} key={fieldName}
            value={formState[fieldName]} 
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
          () => { fetch(endpoint, {method: 'PUT', body:JSON.stringify(formState) }); 
            window.location.reload(false) }
        }> Save edits </Button>
        <Button type="submit" variant="contained" color='error' sx={{float:'right'}} onClick={
          () => {fetch(endpoint, {method:'DELETE'}); redirect("/" + parentType); window.location.reload(false) }
        }> Delete {parentType}</Button>
      </AccordionDetails>
    </Accordion>
  )
}



function AutofillField( {options, autocompleteProps} ){
  return(
  <Autocomplete
    className='autocomplete'
    {...autocompleteProps}
    isOptionEqualToValue={(option, value) => option.id === value.id} // hack!
    options={options}
    renderTags={(value, getTagProps) => 
      value.map((option, index) => {
        let chipLabel = option.label
        if (typeof(option) === 'string') {chipLabel = option}
        return <Chip variant="outlined" label={chipLabel} {...getTagProps({ index })} />
      }
      )
    }
    renderInput={(params) => <TextField multiple {...params} label={autocompleteProps.label} />} >
  </Autocomplete>
  )
}




function AddAndRemoveOptions( {label, addAutoComplete, removeAutocomplete, makeEndpointURL} ) {
  const [fieldState, setFieldState] = useState( {add:[], remove:[]})

  return <>
    <AutofillField 
      options={addAutoComplete}
      autocompleteProps={{
        multiple: true,
        label:'Add ' + label ,
        onChange: (e, value) => setFieldState({...fieldState, add:value})
      }}
    />
    <Button 
      variant='contained'
      onClick={(e)=>{
        for (const toAdd of fieldState.add) {
          fetch( makeEndpointURL(toAdd.id), {method:'PUT'} )
        }
        window.location.reload(false) }}>
      Add
    </Button>
    <AutofillField
      options={removeAutocomplete}
      autocompleteProps={{
        multiple: true,
        label:'Remove ' + label,
        onChange: (e, value) => setFieldState({...fieldState, remove:value})
      }}
    />
    <Button
      variant='contained'
      onClick={(e)=>{
        for (const toRemove of fieldState.remove) {
          fetch( makeEndpointURL(toRemove.id), {method:'DELETE'} )
        }
        window.location.reload(false)}}> 
      Remove
    </Button>
  </>

}


function TopicCards( {topics, comments} ) {
  const cardsToRender = topics.map( (topic) => 
    <Chip 
    className='topic-chips'
    key={topic.id} 
    label={topic.name} 
    href={'/topic/' + topic.id}>
    </Chip>
  )
  return (<>
    {cardsToRender}
  </>)
}






export {EditPanel, AutofillField, TopicCards, AddAndRemoveOptions};





