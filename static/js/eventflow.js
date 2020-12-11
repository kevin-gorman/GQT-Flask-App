import React from "react";
import { Component } from "react";
import { render } from "react-dom";
import { App } from "@data-ui/event-flow";

// forms require this import
import "@data-ui/forms/build/react-select.min.css";


// Function for making the data-ui EventFlow chart
function Eventflow() {
  var adjustedData = [];
  console.log(__dirname);
  var formatDate = d3.timeParse("%Y-%m-%d");

   // Put the event data in the format that data-ui wants
  d3.dsv("|", "/static/data/eventflow_selected_types_v1/events.txt").then(function(data){
    
    
    for (var i = 1; i < data.length; i++) {
        var d = data[i];

        d.Completed = (d.EventAttributes.includes("Completed") ? 'Completed' : 'Missed');
        if (d.EventCategory.includes("Vid")) {
            d.Virtual = "Virtual";
        }
        else if (d.EventCategory.includes("Mes")) {
            d.Virtual = "Message";
        }
        else {
            d.Virtual = "In-Person";
            d.EventCategory = (d.EventCategory.includes("Hom") ? 'Home Visit' : d.EventCategory);
        }

        
        adjustedData[i] = {'ENTITY_ID' : data[i].GUID};
        adjustedData[i].EVENT_NAME = data[i].EventCategory.concat(" ").concat(data[i].Completed);
        adjustedData[i].TS = new Date(data[i].StartTime);
        
    }

    
  });
  
  return <App data={adjustedData} width={1200} height={900} initialMinEventCount={25}/>;

}


render(<Eventflow />, document.getElementById("root"));