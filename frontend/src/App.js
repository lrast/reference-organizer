import './App.css';
import './styles.css'

import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react"

import Home from './Home/home';
import PagesList from './PagesList/pageslist'
import TopicsList from './TopicsList/topicslist'
import RelationshipsList from './RelationshipsList/relationshipslist'
import PageView from './PageView/pageview'
import TopicView from './TopicView/topicview'
import AddPage from './AddPage/addpage'

import { Tab, Box } from '@mui/material'
import {TopicContext, PageContext, AllTopics, AllPages} from './DataContext'

function App() {
  const [topicsData, setTopicsData] = useState([])
  const [pagesData, setPagesData] = useState([])

  useEffect( () => {
    fetch( '/api/topic/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (tableData) => setTopicsData(tableData) )
  }, [])

  useEffect( () => {
    fetch( '/api/page/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (tableData) => setPagesData(tableData) )
  }, [])


  return (
    <>
        <Box sx={{ borderBottom: 2, borderColor: 'divider' }}>
          <Tab label='Home' to="/home" component={Link}/> 
          <Tab label='Pages' to="/page" component={Link}/>
          <Tab label='Topics' to="/topic" component={Link}/>
          <Tab label='Relationships' to="/relationship" component={Link}/>
        </Box>

      <AllTopics.Provider value={topicsData}>
      <AllPages.Provider value={pagesData}>
      <TopicContext.Provider value={topicsData}>
      <PageContext.Provider value={pagesData}>
        <Routes>
          <Route index element={<Home />} />
          <Route path="home" element={<Home />} />
          <Route path="page" element={<PagesList/>}/>
          <Route path="topic" element={<TopicsList/>}/>
          <Route path="relationship" element={<RelationshipsList/>}/>
          <Route path="page/:pageId" element={<PageView/>}/>
          <Route path="topic/:topicId" element={<TopicView/>}/>
          <Route path="newpage" element={<AddPage/>}/>
        </Routes>
      </PageContext.Provider>
      </TopicContext.Provider>
      </AllPages.Provider>
      </AllTopics.Provider>
    </>
  );
}

export default App;
