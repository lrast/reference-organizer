// General use components

import React, {useState, useEffect} from 'react'
import { useNavigate } from "react-router-dom";
import { Accordion, AccordionSummary, AccordionDetails, Autocomplete, TextField, Chip, Button} from '@mui/material';



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
  const navigate = useNavigate()
  return (
  <>
    {topics.map( (topic) => 
        <Chip 
        clickable
        className='topic-chips'
        key={topic.id} 
        label={topic.name} 
        onClick={() => navigate(`../topic/${topic.id}`)}
        >
      </Chip>
    )}
  </>
  )
}


function CommentsPanel({commentURL}) {
  const [commentText, setCommentText] = useState('')

  useEffect( () => {
    fetch(commentURL)
    .then( (resp) => resp.json() )
    .then( (data) => {if(data.length>0){setCommentText(data[0].commentdata) } } )
  }, [])

  return (
    <div className='page-center'>
      <TextField 
          multiline 
          value={commentText}
          InputProps = {{ onChange: (event) => setCommentText( event.target.value )}}
          onBlur={ () => fetch(commentURL +'?commentid=0', 
            {method:'PUT', body: JSON.stringify( {commentdata: commentText } ) }) }
          className='comment-field'
          rows={4}
        />
    </div>
    )
}








export {EditPanel, AutofillField, TopicCards, AddAndRemoveOptions, CommentsPanel};





