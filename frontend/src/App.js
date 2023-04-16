import './App.css';
import './styles.css'

import {
  Routes,
  Route,
  Link
} from "react-router-dom";


import Home from './Home/home';
import PagesList from './PagesList/pageslist'
import TopicsList from './TopicsList/topicslist'
import RelationshipsList from './RelationshipsList/relationshipslist'
import PageView from './PageView/pageview'
import TopicView from './TopicView/topicview'
import AddPage from './AddPage/addpage'


function App() {
  return (
    <>
      <nav className="navheader">
        <li className="navheader"> <Link to="/home">Home</Link> </li>
        <li className="navheader"> <Link to="/page">Pages</Link> </li>
        <li className="navheader"> <Link to="/topic">Topic</Link> </li>
        <li className="navheader"> <Link to="/relationship">Relationships</Link> </li>
      </nav>

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
    </>
  );
}

export default App;
