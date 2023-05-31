import React, {useState, useEffect, useContext} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails, 
        Button, TextField,
        ToggleButtonGroup, ToggleButton} from '@mui/material';

import {EditPanel, AutofillField, TopicCards, AddAndRemoveOptions, CommentsPanel} from '../myComponents';

import PagesTable from '../pagesTable'

import {TopicContext, PageContext} from '../DataContext'

import {OpenPageLink} from '../utilities'


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

  const [toggleSide, setToggleSide] = useState('left')
  const [relatedPages, setRelatedPages] = useState( {pages:[], opposite:'right', label:'cited page'} )

  useEffect( () =>{
    if (toggleSide === 'left'){
      setRelatedPages({pages: pageData[ 'leftPages' ], opposite:'right', label:'cited page'})
    }
    else if (toggleSide === 'right'){
      setRelatedPages({pages: pageData[ 'rightPages' ], opposite:'left', label:'citing page'})
    }
  }, [pageData, toggleSide])



  return (
    <>
    <center> <h1> <OpenPageLink page={pageData} /> </h1> </center>
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
        <ToggleButtonGroup
          value={toggleSide}
          onChange={ (e, newState) => setToggleSide(newState) }
          exclusive
        >
          <ToggleButton value="left"> Cited pages </ToggleButton>
          <ToggleButton value="right"> Citing pages </ToggleButton>
        </ToggleButtonGroup>


        <PageContext.Provider value={relatedPages['pages']}>
          <PagesTable />

          <AddAndRemoveOptions
            label={ relatedPages['label'] }
            addAutoComplete={useContext(PageContext).map((obj) => ({...obj, label:obj.name})) }
            removeAutocomplete={relatedPages['pages'].map((obj) => ({...obj, label:obj.name}))}
            makeEndpointURL={(id) => '/api/page/'+pageId+'/page/'+id+
              '?primaryside='+relatedPages['opposite'] }
          />

        </PageContext.Provider>
      </AccordionDetails>
    </Accordion>

    <EditPanel parentType="page" parentData={pageData} />
    </>
    )
}

export default PageView;