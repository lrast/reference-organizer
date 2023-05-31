// utility functions

import {backendURL} from './config'

function unpackGQL(data, model, uniqueIds=true) {
  // unpack graphql results

  function unpackHelper(data, model){
    if (model.length === 1) {
      return data[model[0]]
    }

    let dataList = data[ model[0] ]
    let unpackedList = dataList.map( (obj) => unpackGQL( obj, model.slice(1) ) )

    return unpackedList.reduce( (acc, li) => [...acc, ...li], [] )
  }

  let unpackedItems = unpackHelper(data, model)

  // handle unique and sorting
  if (uniqueIds){
    let allIds = unpackedItems.map( x=>x.id )
    unpackedItems = unpackedItems.filter( 
      (item, pos) => ( allIds.indexOf( item.id ) === pos)
    )
  }

  return unpackedItems
}

function OpenPageLink({page}){
  if (page.url === ''){
    return <> {page.name} </>
  }
  else {
    return  <a href={backendURL +'/openpage/' + page.id}> {page.name} </a>
  }

}




export {unpackGQL, OpenPageLink};