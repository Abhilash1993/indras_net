import React from "react";
import ReactJson from 'react-json-view'


function Debugger(props){
    let data = props.envFile
    console.log(data)
    if (props.loadingData){
        console.log("inside Debugger")
        return(
        <ReactJson src={data} />
        )
    }
    else {
        return (null)
    }
}

export default Debugger;