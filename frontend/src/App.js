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

import {TopicContext, PageContext} from './DataContext'

function App() {
  const [allTopics, setAllTopics] = useState([])
  const [allPages, setAllPages] = useState([])

  useEffect( () => {
    fetch( '/api/topic/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (tableData) => setAllTopics(tableData) )
  }, [])

  useEffect( () => {
    fetch( '/api/page/')
    .then( (response) => response.json())
    .then( (rawData) => rawData.sort( (a,b) => ((a.name.toLowerCase() > b.name.toLowerCase()) - 0.5) ) )
    .then( (tableData) => setAllPages(tableData) )
  }, [])


  return (
    <>
      <nav className="navheader">
        <li className="navheader"> <Link to="/home">Home</Link> </li>
        <li className="navheader"> <Link to="/page">Pages</Link> </li>
        <li className="navheader"> <Link to="/topic">Topics</Link> </li>
        <li className="navheader"> <Link to="/relationship">Relationships</Link> </li>
      </nav>

      <TopicContext.Provider value={allTopics}>
      <PageContext.Provider value={allPages}>
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
    </>
  );
}

export default App;
