import React from 'react'
import { useParams } from 'react-router-dom';

function TopicView() {
    let {topicId} = useParams()
    return <div> Topic View {topicId}</div>
}

export default TopicView;