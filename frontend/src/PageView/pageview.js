import React, {useState, useEffect, useContext} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails, Button } from '@mui/material';

import {EditPanel, AutofillField} from '../myComponents';

import TopicsTable from '../topicsTable'
import PagesTable from '../pagesTable'

import {TopicContext, PageContext} from '../DataContext'

import { Link } from "react-router-dom";

import {backendURL} from '../config'


function PageView() {
  let {pageId} = useParams()
  const [pageData, setData] = useState(
    {id:"", url:"", name:"", dateadded:"", topics:[], leftPages:[], rightPages:[] }
  )

  useEffect( () => {
      fetch('/api/page/'+ pageId )
      .then( (response) => response.json() )
      .then( (data) => {setData(data) })
    }, [])


  const [fieldState, setFieldState] = useState( {add:'', remove:''})


  return (
    <>
    <center> <h1> <Link to={backendURL+ '/openpage/' + pageId }> {pageData.name } </Link> </h1> </center>
    <Accordion defaultExpanded={true}>
      <AccordionSummary>
        <h2> Topics </h2>
      </AccordionSummary>
      <AccordionDetails>
        <TopicContext.Provider value={pageData.topics}>
          <TopicsTable />
        </TopicContext.Provider>

        <AutofillField options={useContext(TopicContext).map((obj) => ({...obj, label:obj.name})) }
        autocompleteProps={{
          multiple: true,
          label:'Add Topics',
          onChange: (e, value) => setFieldState({...fieldState, add:value})
        }}/>
        <Button variant='contained'
          onClick={(e)=>{
            for (const topicToAdd of fieldState.add) {
              fetch('/api/page/'+pageId+'/topic/'+topicToAdd.id, {method:'PUT'} )
            }
            window.location.reload(false)
          }}
        > Add </Button>
        <AutofillField options={pageData.topics.map((obj) => ({...obj, label:obj.name}))}
        autocompleteProps={{
          multiple: true,
          label:'Remove Topics',
          onChange: (e, value) => setFieldState({...fieldState, remove:value})
        }}/>
        <Button variant='contained'
          onClick={(e)=>{
            for (const topicToAdd of fieldState.remove) {
              fetch('/api/page/'+pageId+'/topic/'+topicToAdd.id, {method:'DELETE'} )
            }
            window.location.reload(false)
          }}
        > Remove </Button>



      </AccordionDetails>
    </Accordion>

    <Accordion defaultExpanded={true}>
      <AccordionSummary>
        <h2> Related Pages </h2>
      </AccordionSummary>
      <AccordionDetails>
        <PageContext.Provider value={pageData.leftPages}>
          <PagesTable />
        </PageContext.Provider>
      </AccordionDetails>
    </Accordion>

    <EditPanel parentType="page" parentData={pageData} />
    </>
    )
}

export default PageView;