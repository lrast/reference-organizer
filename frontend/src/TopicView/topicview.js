import React, {useState, useEffect, useContext} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails, Button, TextField} from '@mui/material';

import PagesTable from '../pagesTable'
import TopicsTable from '../topicsTable'

import {EditPanel, AutofillField} from '../myComponents';

import {TopicContext, PageContext} from '../DataContext'

import {unpackGQL} from '../utilities'

function TopicView() {
  let {topicId} = useParams()

  const [topicData, setTopicData] = useState(
    {id:"", name:"", pages:[], leftTopics:[], rightTopics:[], intersectingTopics:[] }
  )

  useEffect( () => {
    fetch( '/api/gql?' + new URLSearchParams(
      {query:`{ topics(id: ${topicId})
        {id, name, 
        pages{id, name}, 
        allSubTopics{id, name, pages{id, name, topics{id, name} }},
        rightTopics{id, name},
        leftTopics{id, name} 
      }}`
    }) )
    .then( (resp) => resp.json() )
    .then( (data) => data.topics[0] )
    .then( (data) => {
      let intersectingTopics = unpackGQL(data, ['allSubTopics', 'pages', 'topics'])
      const intIDs = intersectingTopics.map( (e) =>e.id )

      intersectingTopics = intersectingTopics.filter( 
        (v,i) => intIDs.indexOf(v.id) == i 
        ).sort( 
        (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5)
        )

      setTopicData( {
        id: data.id, name: data.name,
        pages: unpackGQL(data, ['allSubTopics', 'pages']),
        intersectingTopics: intersectingTopics,
        leftTopics: data.leftTopics, rightTopics: data.rightTopics
      })
    })
  }, [] )


  const [commentText, setCommentText] = useState('')

  useEffect( () => {
    fetch('/api/comment/topic/' +topicId)
    .then( (resp) => resp.json() )
    .then( (data) => setCommentText(data[0].commentdata) )
  }, [])

  const [fieldState, setFieldState] = useState( {add:'', remove:''})

  return (
    <>
    <center> <h1> {topicData.name} </h1> </center>

    <TextField multiline value={commentText}
      InputProps = {{ onChange: (event) => setCommentText( event.target.value )}}
      onBlur={() => fetch('/api/comment/topic/' +topicId +'?commentid=0', 
        {method:'PUT', body: JSON.stringify( {commentdata: commentText } ) })}
    />

    <Accordion defaultExpanded={true}>
      <AccordionSummary>
        <h2> Pages </h2>
      </AccordionSummary>
      <AccordionDetails>
        <PageContext.Provider value={topicData.pages}>
        <TopicContext.Provider value={topicData.intersectingTopics}>
          <PagesTable />
        </TopicContext.Provider>
        </PageContext.Provider>
      </AccordionDetails>
    </Accordion>

   <Accordion defaultExpanded={true}>
      <AccordionSummary>
        <h2> Related Topics </h2>
      </AccordionSummary>
      <AccordionDetails>
        <TopicContext.Provider value={topicData.leftTopics}>
          <TopicsTable />
        </TopicContext.Provider>
        <AutofillField options={useContext(TopicContext).map((obj) => ({...obj, label:obj.name})) }
        autocompleteProps={{
          multiple: true,
          label:'Add Subtopics',
          onChange: (e, value) => setFieldState({...fieldState, add:value})
        }}/>
        <Button variant='contained'
          onClick={(e)=>{
            for (const topicToAdd of fieldState.add) {
              fetch('/api/topic/'+topicId+'/topic/'+topicToAdd.id+'?primaryside=right', {method:'PUT'} )
            }
            window.location.reload(false)
          }}
        > Add </Button>
        <AutofillField options={topicData.leftTopics.map((obj) => ({...obj, label:obj.name}))}
        autocompleteProps={{
          multiple: true,
          label:'Remove Subtopics',
          onChange: (e, value) => setFieldState({...fieldState, remove:value})
        }}/>
        <Button variant='contained'
          onClick={(e)=>{
            for (const topicToRemove of fieldState.remove) {
              fetch('/api/topic/'+topicId+'/topic/'+topicToRemove.id+'?primaryside=right', {method:'DELETE'} )
            }
            window.location.reload(false)
          }}
        > Remove </Button>
      </AccordionDetails>
    </Accordion>



    <EditPanel parentType="topic" parentData={topicData}/>
    </>
  )
}


export default TopicView;