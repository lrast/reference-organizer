import {useState, useEffect, useRef, useMemo, useContext} from 'react';

import {AutofillField} from './myComponents'
import {TextField, Button, Checkbox, IconButton, Grid, Switch,FormControlLabel} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

import {useTable, useFilters, useGlobalFilter} from 'react-table'
import {matchSorter} from 'match-sorter'

import {TopicContext, PageContext, TableType} from './DataContext'


// table component
function TableBody({data, columns, allFilters, searchString, hiddenColumns=[]}) {
  // Responsible for rendering a table

  data = useMemo( () => data, [data])
  columns = useMemo( () => columns, [columns] )

  const defaultColumn = useMemo(
    () => ({
      Filter: () => {}
    }),
    []
  )

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    setAllFilters,
    setGlobalFilter
  } = useTable({ columns, data, defaultColumn, 
      initialState: {
        hiddenColumns: hiddenColumns,
        filters: [
            {
              id: 'id',
              value: {in: null, out:null}
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
    setAllFilters( [{id:'id', value: allFilters }])
  }, [allFilters])


    return (
        <table {...getTableProps()} className="reference-table">
         <thead>
           {headerGroups.map(headerGroup => (
             <tr {...headerGroup.getHeaderGroupProps()}>
               {headerGroup.headers.map(column => {
                return <th {...column.getHeaderProps()}> {column.render('Header')} </th>
               }
              )}
             </tr>
           ))}
         </thead>
         <tbody {...getTableBodyProps()} className='table-body'>
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
   )
}




// table sidebar
function Sidebar({searchString, setSearchString, setFilterValues} ) {
  // Responsible for rendering and updating the values of the filters

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

  // collate the filter bank to produce a single output
  useEffect( () => {
    let collatedFilter = {in: null, out:null}

    for (const individualFilter of filterBank.filter(f => (!(f.payload === null )) ) )
    {
      const filterData = individualFilter.payload

      if (filterData.in){
        if (collatedFilter.in === null) {collatedFilter.in=[]}
        collatedFilter.in = [...collatedFilter.in, ...filterData.in]
      }
      if (filterData.out){
        if (collatedFilter.out === null) {collatedFilter.out=[]}
        collatedFilter.out = [...collatedFilter.out, ...filterData.out]
      }
    }

    setFilterValues(collatedFilter)
  }, [filterBank])


  return (
    <div className="table-sidebar">
      <TextField type="text" name="test" label="Search"   className="search-filter"
        value={searchString}
        InputProps = {{
          onChange: (event) => {
            setSearchString( event.target.value )
          }
        }}
       />
        {filterComponents}
      <div className="new-filter-button" >
      <Button variant="contained" onClick={() => {
        let thisKey = Math.max( ...filterComponents.map( (item) =>(item.key) ), 0 ) + 1 + ''
        setFilterComponents( [...filterComponents,
          <FilterComponentBody 
            key={thisKey} myKey={thisKey}
            removeSelf={()=> removeFilterByKey(thisKey)} updateFilter={updateFilterBank}
          />
        ])
      }} > New Filter</Button>
      </div>
    </div>
  )
}




function FilterComponentBody({myKey, removeSelf, updateFilter}) {

  // pull context information
  const tableType = useContext(TableType)
  const autocompleteTopics = useContext(TopicContext).map( (obj) => {return {...obj, label:obj.name} } )
  const autocompletePages = useContext(PageContext).map( (obj) => {return {...obj, label:obj.name} } )


  // set up filter state
  const [ uiState, setUiState ] = useState(
    { filterIn: true, subtopics: true, filterQuery: [],
      filterOn: "topics", inputLabel:"Filter In"
    }
  )

  // filter parser function
  const [loadedData, setLoadedData] = useState( null )
  function parseFilter( form ) {
    let outputKey = 'out'
    if (form.filterIn) {outputKey='in'}

    function unpackGQL(data, model) {
      // unpack graphql results
      if (model.length === 0) {
        return [data.id]
      }

      let dataList = data[ model[0] ]
      let unpackedList = dataList.map( (obj) => unpackGQL( obj, model.slice(1) ) )
      return unpackedList.reduce( (acc, li) => [...acc, ...li] )
    }

    // begin
    if (form.filterQuery.length === 0) { setLoadedData(null); return }

    if (form.filterOn === tableType) {
      // same table type
      if (form.subtopics) {
        // fetch subtopic data
        fetch('/api/gql?' + new URLSearchParams(
          {query: `{ ${form.filterOn} (ids: [${form.filterQuery}] ) { allSubTopics { id, name }} }` }) )
        .then( (resp) => resp.json())
        .then( (data) => unpackGQL(data, [form.filterOn, 'allSubTopics']) )
        .then( (ids) => setLoadedData( {[outputKey]: ids} ) )
      }
      else {
        setLoadedData( {[outputKey]: form.filterQuery} )
      }
    }
    else {
      // opposite table type
      if (form.subtopics) {
        // fetch subtopic data
        fetch('/api/gql?' + new URLSearchParams(
          {query: `{ ${form.filterOn} (ids: [${form.filterQuery}] ) { allSubTopics { ${tableType} { id} }} }` }) )
        .then( (resp) => resp.json())
        .then( (data) => unpackGQL(data, [form.filterOn, 'allSubTopics', tableType]) )
        .then( (ids) => setLoadedData( {[outputKey]: ids} ) )
      }
      else {
        fetch('/api/gql?' + new URLSearchParams(
          {query: `{ ${form.filterOn} (ids: [${form.filterQuery}] ) { ${tableType} { id} }}` }) )
        .then( (resp) => resp.json())
        .then( (data) => unpackGQL(data, [form.filterOn, tableType]) )
        .then( (ids) => setLoadedData( {[outputKey]: ids} ) )
      }
    }
  }


  // need to update the filter state when the ui state changes
  useEffect( () => {
    parseFilter(uiState)
  }, [uiState] )

  useEffect( () => {
    updateFilter({filterId: myKey, payload:loadedData} )
  }, [loadedData])



  return (
    <div className="sidebar-filter-body">
      <div className="sidebar-filter-exit">
      <IconButton onClick={removeSelf}>
        <CloseIcon />
      </IconButton>
      </div>

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
        control={<Checkbox defaultChecked
          onChange={ (e) => { setUiState( {...uiState, subtopics:e.target.checked }) }}
        />}
        label="Include Subtopics"
      />
      <AutofillField options={autocompleteTopics}
            autocompleteProps={{
            label:uiState.inputLabel,
            multiple:true,
            onChange: (e, value) => {setUiState({...uiState, filterQuery:value.map( (x) => x.id ) }) } 
        }}
      />
    </div> 
  )
}




export {TableBody, Sidebar};
