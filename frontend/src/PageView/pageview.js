import React, {useState, useEffect, useContext} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails, Button, TextField} from '@mui/material';

import {EditPanel, AutofillField, TopicCards, AddAndRemoveOptions, CommentsPanel} from '../myComponents';

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
      .then( (data) => {setData(data)})
    }, [])


  return (
    <>
    <center> <h1> <Link to={backendURL+ '/openpage/' + pageId }> {pageData.name } </Link> </h1> </center>
    <CommentsPanel commentURL={'/api/comment/page/' + pageId} />

    <Accordion defaultExpanded={true}>
      <AccordionSummary>
        <h2> Topics </h2>
      </AccordionSummary>
      <AccordionDetails>
        <TopicCards topics={pageData.topics}/>

        <AddAndRemoveOptions
          label={'Topics'}
          addAutoComplete={useContext(TopicContext).map((obj) => ({...obj, label:obj.name})) }
          removeAutocomplete={pageData.topics.map((obj) => ({...obj, label:obj.name}))}
          makeEndpointURL={(id) => '/api/page/'+pageId+'/topic/'+ id }
        />



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