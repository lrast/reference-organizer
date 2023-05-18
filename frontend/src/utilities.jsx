// utility functions

function unpackGQL(data, model, unique=true) {
    // unpack graphql results
    if (model.length == 1) {
      return data[model[0]]
    }

    let dataList = data[ model[0] ]
    let unpackedList = dataList.map( (obj) => unpackGQL( obj, model.slice(1) ) )

    // handle unique and sorting
    if (unique){}

    return unpackedList.reduce( (acc, li) => [...acc, ...li] )
}

export {unpackGQL};