import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom';

import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';

import {Sidebar, TableBody} from '../TableComponents'
import {EditPanel} from '../myComponents';

function TopicView() {
  let {topicId} = useParams()
  const [topicData, setData] = useState({})

  const [pageTableData, setPageTableData] = useState([])
  const [pageCols, setPageCols] = useState([])


  useEffect( () => {
  fetch( '/api/topic/' + topicId )
  .then( (response) => response.json() )
  .then( (data) => {
    setData(data);
    setPageTableData( data.pages.map( (row) => { return {
      'link': <a> {row.name} </a>,
      'info': <a href={'/page/'+row.id}> info </a>,
      'remove': <a> Remove from topic </a>
    }}) );
    setPageCols([
      { Header: '', accessor: 'link'},
      {Header: '', accessor: 'info'},
      { Header: '', accessor: 'remove'}
      ])
  })
  }, [])

  return (
    <>
    <center> <h1> {topicData.name} </h1> </center>
    <Accordion defaultExpanded="true">
      <AccordionSummary>
        <h2> Pages </h2>
      </AccordionSummary>
      <AccordionDetails>
        <div className="table-wrapper">
          <TableBody data={pageTableData} columns={pageCols}/>
          <Sidebar/>
        </div>
      </AccordionDetails>
    </Accordion>

   <Accordion defaultExpanded="true">
      <AccordionSummary>
        <h2> Related Topics </h2>
      </AccordionSummary>
      <AccordionDetails>
        MORE!
      </AccordionDetails>
    </Accordion>

    <EditPanel rootType="topic" rootId={topicId}/>
    </>
  )
}


export default TopicView;