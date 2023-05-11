import { createContext } from 'react';

const TopicContext = createContext([])
const PageContext = createContext([])

const AllTopics = createContext([])
const AllPages = createContext([])

const TableType = createContext("")

export {TopicContext, PageContext, AllTopics, AllPages, TableType}


