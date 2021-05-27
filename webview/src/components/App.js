import React from 'react'
import '../styles/styles.css'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'

function App() {
  return (
    /*
    -- FRESH START --
    To remove the landing page components just replace the returned code below by the following:

    <Router>
      <div className="flex flex-col min-h-screen ">
        <div className="container flex-grow">
          <p>Your Routes go here!</p>
        </div>
      </div>
    </Router>
    */
    <Router>
      <div className="flex flex-col min-h-screen ">
        <p>React app running!</p>
      </div>
    </Router>
  )
}

export default App
