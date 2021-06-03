import React from 'react'
import '../styles/styles.css'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import MoodPlot from './MoodPlot'
import BackendService from '../services/BackendService'
import Diary from './Diary'
import MockDataService from '../services/MockData'

class App extends React.Component {

  backendService = new BackendService();
  mockDataService = new MockDataService();

  mock = true;

  constructor(props) {
    super(props);
    this.state = { data: null };
    if (this.mock) {
      this.state = {
        data: this.mockDataService.getMockViewdata(),
      }
    }
  }

  componentDidMount() {
    if (!this.mock) {
      var query = new URLSearchParams(window.location.search);

      this.backendService.getWebviewData(query.get("token"), query.get("user")).then(result => {
        this.setState({ data: result });
      });
    }
  }

  render() {
    return (
      <Router>
        <div className="flex flex-col min-h-screen">
          <div className="flex items-center justify-center">
            <MoodPlot data={this.state.data}></MoodPlot>
          </div>
          <div className="flex items-center justify-center">
            <Diary data={this.state.data}></Diary>
          </div>
        </div>
      </Router>
    )
  }
}

export default App;
