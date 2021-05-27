import React from 'react'
import '../styles/styles.css'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import MoodPlot from './MoodPlot'

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen ">
        <div class="flex items-center justify-center h-screen">
          <div class="bg-grey-800 text-white font-bold rounded-lg border shadow-lg p-5">
            <MoodPlot></MoodPlot>
          </div>
        </div>

      </div>
    </Router>
  )
}

export default App
