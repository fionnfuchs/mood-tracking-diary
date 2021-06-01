import React from 'react'
import '../styles/styles.css'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import MoodPlot from './MoodPlot'
import BackendService from '../services/BackendService'

class App extends React.Component {

  backendService = new BackendService();

  constructor(props) {
    super(props);
    this.state = { data: null };
    /* MOCK DATA: this.state = {
      data: {
        moodValues: [
          {
            value: 4,
            timestamp: "01.01.2021"
          },
          {
            value: 1,
            timestamp: "02.01.2021"
          },
          {
            value: 5,
            timestamp: "03.01.2021"
          },
        ]
      }
    }*/


  }

  componentDidMount() {
    var query = new URLSearchParams(window.location.search);

    this.backendService.getWebviewData(query.get("token"), query.get("user")).then(result => {
      this.setState({ data: result });
    });
  }

  render() {
    return (
      <Router>
        <div className="flex flex-col min-h-screen ">
          <div className="flex items-center justify-center h-screen">
            <div className="bg-grey-800 text-white font-bold rounded-lg border shadow-lg p-5">
              <MoodPlot data={this.state.data}></MoodPlot>
            </div>
          </div>
        </div>
      </Router>
    )
  }
}

export default App;
