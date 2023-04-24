import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';

import {EditPanel} from '../myComponents';

function PageView() {
  let {pageId} = useParams()
  const [pageData, setData] = useState({})

  useEffect( () => {
      fetch('/api/page/'+ pageId )
      .then( (response) => response.json() )
      .then( (data) => setData(data) )
    }, [])

  return (
    <>
    <center> <h1> <a href={pageData.url}> {pageData.name } </a> </h1> </center>
    <Accordion defaultExpanded="true">
      <AccordionSummary>
        <h2> Topics </h2>
      </AccordionSummary>
      <AccordionDetails>
        MORE!
      </AccordionDetails>
    </Accordion>

    <Accordion defaultExpanded="true">
      <AccordionSummary>
        <h2> Related Pages </h2>
      </AccordionSummary>
      <AccordionDetails>
        MORE!
      </AccordionDetails>
    </Accordion>

    <EditPanel rootType="page" rootId={pageId} />

    </>
    )
}

export default PageView;