import React from 'react'
import { useParams } from 'react-router-dom';

function PageView() {
    let {pageId} = useParams()
    return <div> Page View {pageId}</div>
}

export default PageView;