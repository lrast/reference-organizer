import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';

import PagesTable from '../pagesTable'
import TopicsTable from '../topicsTable'

import {EditPanel} from '../myComponents';

import {TopicContext, PageContext} from '../DataContext'

function TopicView() {
  let {topicId} = useParams()
  const [topicData, setTopicData] = useState(
    {id:"", name:"", pages:[], leftTopics:[], rightTopics:[] }
  )

  useEffect( () => {
  fetch( '/api/topic/' + topicId )
  .then( (response) => response.json() )
  .then( (data) => {setTopicData(data)} )
  }, [])



  return (
    <>
    <center> <h1> {topicData.name} </h1> </center>
    <Accordion defaultExpanded={true}>
      <AccordionSummary>
        <h2> Pages </h2>
      </AccordionSummary>
      <AccordionDetails>
        <PageContext.Provider value={topicData.pages}>
          <PagesTable />
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
      </AccordionDetails>
    </Accordion>

    <EditPanel parentType="topic" parentData={topicData}/>
    </>
  )
}


export default TopicView;