import {useState, useEffect, useRef, useMemo} from 'react';

import {AutofillField} from './myComponents'
import {TextField, Button, Checkbox, IconButton, Box, Grid, Switch,FormControlLabel} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

import {useTable, useFilters, useGlobalFilter} from 'react-table'
import {matchSorter} from 'match-sorter'



// table component
function TableBody({data, columns, allFilters, searchString, hiddenColumns=[]}) {
  // Responsible for rendering a table

  data = useMemo( () => data, [data])
  columns = useMemo( () => columns, [columns] )

  const defaultColumn = useMemo(
    () => ({
      Filter: () => []
    }),
    []
  )

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    setFilter,
    setAllFilters,
    state,
    setGlobalFilter
  } = useTable({ columns, data, defaultColumn, 
      initialState: {
        hiddenColumns: hiddenColumns,
        filters: [
            {
              id: 'id',
              value: []
            }
          ],
      },
      globalFilter: (rows, id, searchString) => matchSorter(rows, searchString, { keys: ['original.name'] })
      },
  useFilters, useGlobalFilter)


  useEffect( () => {
    setGlobalFilter(searchString)
  }, [searchString])

  useEffect( () => {
    console.log('effect', allFilters)
    if (allFilters) { setAllFilters(allFilters) }

  }, [allFilters])


    return (
      <div className="table-body">
        <Button onClick={() => { 
          console.log( allFilters )
          setAllFilters( [{id:"id", value:[]}] )
        } } > test </Button>
        <table {...getTableProps()} className="reference-table">
         <thead>
           {headerGroups.map(headerGroup => (
             <tr {...headerGroup.getHeaderGroupProps()}>
               {headerGroup.headers.map(column => {
                //console.log(column)
                return <th {...column.getHeaderProps()}> {column.render('Header')} </th>
               }
              )}
             </tr>
           ))}
         </thead>
         <tbody {...getTableBodyProps()}>
           {rows.map(row => {
             prepareRow(row)
             return (
               <tr {...row.getRowProps()} className="wide-column" >
                 {row.cells.map(cell => {
                   return (
                     <td{...cell.getCellProps()}>
                       {cell.render('Cell')}
                     </td>
                   )
                 })}
               </tr>
             )
           })}
         </tbody>
        </table>
      </div>
   )
}




// table sidebar
function Sidebar({searchString, setSearchString, setFilterValues} ) {
  // Responsible for rendering and updating the values of the filters

  // preload topic data
  const [allTopics, setTopics] = useState([])
  const [allPages, setPages] = useState([])

  useEffect( () => {
    fetch('/api/topic/')
    .then( (response) => response.json())
    .then( (options) => options.map( 
      (propertiesDict) => {
        propertiesDict['label'] = propertiesDict['name']
        return propertiesDict 
      } ) )
    .then( (options) => options.sort( (a,b) => (a.label.toLowerCase() > b.label.toLowerCase())-0.5 ) )
    .then( (options) => setTopics(options)  )
  }, [])

  // state of the sidebar of filters
  const [filterComponents, setFilterComponents] = useState([])
  const [filterBank, setFilterBank] = useState([])

  // state references
  const filterComponentsRef = useRef()
  filterComponentsRef.current = filterComponents;

  const filterBankRef = useRef()
  filterBankRef.current = filterBank

  const removeFilterByKey = (key) => {
    setFilterComponents( filterComponentsRef.current.filter( (item) => (item.key != key) ) )
    setFilterBank( filterBankRef.current.filter( (i) => (i.filterId != key) ) )
  }

  const updateFilterBank = (filterElement) => {
    setFilterBank( 
      [...filterBankRef.current.filter( (i) => (i.filterId != filterElement.filterId) ), 
        filterElement ] 
    )
  }

  function computeInclusionExclusion( filters ){
    const appendQuery = (acc, ele) => {acc.push(...ele.filterQuery); return acc}

    let inIds = [... new Set( filters.filter( (x) => (x.filterIn) ).reduce(appendQuery, []) )]
    let outIds = [... new Set( filters.filter( (x) => (! x.filterIn) ).reduce(appendQuery, []) )]

    return {in: inIds, out:outIds}
  }


  // collate the filter bank to produce a single output
  useEffect( () => {
    let collatedFilter = {
      topic: computeInclusionExclusion(filterBank.filter( (x) => (x.filterOn == "topic") ) ),
      page: computeInclusionExclusion(filterBank.filter( (x) => (x.filterOn == "page") ) )
    }
    setFilterValues(collatedFilter)

  }, [filterBank])


  return (
    <div className="table-sidebar">
      <TextField type="text" name="test" label="Search" className="sidebar-filter-body"
        value={searchString}
        InputProps = {{
          onChange: (event) => {
            setSearchString( event.target.value )
          }
        }}
       />
      <ul style={{listStyle: "none"}}>
        {filterComponents}
      </ul>
      <Button variant="contained" onClick={() => {
        let thisKey = Math.max( ...filterComponents.map( (item) =>(item.key) ), 0 ) + 1 + ''
        setFilterComponents( [...filterComponents,
          <FilterComponentBody 
            key={thisKey} myKey={thisKey}
            removeSelf={()=> removeFilterByKey(thisKey)} updateFilter={updateFilterBank}
            loadedTopics={allTopics} 
          />
        ])
      }} > New Filter</Button>
    </div>
  )
}






function FilterComponentBody({myKey, removeSelf, updateFilter, loadedTopics}) {
  // sets up blank filter element
  const [ uiState, setUiState ] = useState(
    { filterIn: true, subtopics: false, filterQuery: [],
      filterOn: "topic", filterId: myKey,
      inputLabel:"Filter In"
    }
  )

  // need to update the filter state when the ui state changes
  useEffect( () => {
    updateFilter( uiState )
  }, [uiState] )

  return (
    <li className="sidebar-filter-item" key='test'>
    <div className="sidebar-filter-body" key='test'>
      <IconButton onClick={removeSelf} >
        <CloseIcon />
      </IconButton>

      <Grid component="label" container alignItems="center" spacing={0}>
        <Grid item>Out</Grid>
        <Grid item>
          <Switch
            onChange={ (e) => {
              let labelValue = "Filter Out"
              if (e.target.checked) {labelValue = "Filter In"}
              setUiState( {...uiState, filterIn:e.target.checked, inputLabel:labelValue} )
            }}
            defaultChecked
          />
        </Grid>
        <Grid item>In</Grid>
      </Grid>

      <FormControlLabel 
        control={<Checkbox 
          onChange={ (e) => { setUiState( {...uiState, subtopics:e.target.checked }) }}
        />}
        label="Include Subtopics"
      />
      <AutofillField preLoaded={loadedTopics}
            autocompleteProps={{
            label:uiState.inputLabel,
            multiple:true,
            onChange: (e, value) => {setUiState({...uiState, filterQuery:value.map( (x) => x.id ) }) } 
        }}
      />
    </div>
    </li> )
}


export {TableBody, Sidebar };
