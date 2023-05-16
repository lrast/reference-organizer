import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';

import PagesTable from '../pagesTable'
import TopicsTable from '../topicsTable'

import {EditPanel} from '../myComponents';

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




  return (
    <>
    <center> <h1> {topicData.name} </h1> </center>
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
      </AccordionDetails>
    </Accordion>

    <EditPanel parentType="topic" parentData={topicData}/>
    </>
  )
}


export default TopicView;