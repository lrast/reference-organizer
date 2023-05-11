import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';

import {EditPanel} from '../myComponents';

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