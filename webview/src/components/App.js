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
        this.setState({ data: result, loaded: true });
      });
    }
  }

  render() {
    var webview = <div className="flex flex-col min-h-screen">
      <div className="flex items-center justify-center">
        <div class="w-full lg:w-1/2 2xl:w-1/3 py-4 px-8 bg-white shadow-lg rounded-lg my-10">
          <h1 class="text-gray-800 text-4xl font-semibold">Loading...</h1>
          <p>Loading your data - please wait a moment...</p>
        </div>
      </div>
    </div>;

    if (this.state.data && this.state.data.diaryEntries && this.state.data.diaryEntries.length > 0) {

      webview = <div className="flex flex-col min-h-screen">
        <div className="flex items-center justify-center">
          <div className="w-full lg:w-1/2 2xl:w-1/3 py-4 px-8 bg-white shadow-lg rounded-lg my-10">
            <h1 className="text-gray-800 text-4xl font-semibold">Your Mood Diary and Stats</h1>
            <p className="text-red-700">You should not share this link with anybody!</p>
          </div>
        </div>
        <div className="flex items-center justify-center">
          <MoodPlot data={this.state.data}></MoodPlot>
        </div>
        <div className="flex items-center justify-center">
          <Diary data={this.state.data}></Diary>
        </div>
      </div>;

    } else if (this.state.loaded) {

      webview = <div className="flex flex-col min-h-screen">
        <div className="flex items-center justify-center">
          <div className="w-full lg:w-1/2 2xl:w-1/3 py-4 px-8 bg-white shadow-lg rounded-lg my-10">
            <h1 className="text-gray-800 text-4xl font-semibold">Invalid Link</h1>
            <p>Generate a new one by sending /stats to the Modia bot!</p>
          </div>
        </div>
      </div>;

    }

    return (
      <Router>
        {webview}
      </Router>
    )
  }
}

export default App;
