import React, {useState, useEffect, useContext} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails, Button, TextField} from '@mui/material';

import PagesTable from '../pagesTable'
import TopicsTable from '../topicsTable'

import {EditPanel, AutofillField, TopicCards, AddAndRemoveOptions, CommentsPanel} from '../myComponents';

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
  }, [topicId] )


  return (
    <>
    <center> <h1> {topicData.name} </h1> </center>
    <CommentsPanel commentURL={'/api/comment/topic/' + topicId} />
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
        <AddAndRemoveOptions
            label={'Pages'}
            addAutoComplete={useContext(PageContext).map((obj) => ({...obj, label:obj.name})) }
            removeAutocomplete={topicData.pages.map((obj) => ({...obj, label:obj.name}))}
            makeEndpointURL={(id) => '/api/topic/'+topicId+'/page/'+id }
          />
      </AccordionDetails>
    </Accordion>

   <Accordion defaultExpanded={true}>
      <AccordionSummary>
        <h2> Related Topics </h2>
      </AccordionSummary>
      <AccordionDetails>

        <div> 
          <h3> Subtopics </h3>
          <TopicCards topics={topicData.leftTopics}/>
          <AddAndRemoveOptions
            label={'Subtopics'}
            addAutoComplete={useContext(TopicContext).map((obj) => ({...obj, label:obj.name})) }
            removeAutocomplete={topicData.leftTopics.map((obj) => ({...obj, label:obj.name}))}
            makeEndpointURL={(id) => '/api/topic/'+topicId+'/topic/'+id+'?primaryside=right' }
          />
        </div>

        <div> 
          <h3> Supertopics </h3>
          <TopicCards topics={topicData.rightTopics} className="topic-cards"/>
          <AddAndRemoveOptions
            label={'Supertopics'}
            addAutoComplete={useContext(TopicContext).map((obj) => ({...obj, label:obj.name})) }
            removeAutocomplete={topicData.rightTopics.map((obj) => ({...obj, label:obj.name}))}
            makeEndpointURL={(id) => '/api/topic/'+topicId+'/topic/'+id+'?primaryside=left' }
          />

        </div>
      </AccordionDetails>
    </Accordion>



    <EditPanel parentType="topic" parentData={topicData}/>
    </>
  )
}


export default TopicView;