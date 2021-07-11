import React from 'react';
import '../styles/styles.css';
import { BrowserRouter as Router } from 'react-router-dom';
import MoodPlot from './MoodPlot';
import BackendService from '../services/BackendService';
import Diary from './Diary';
import MockDataService from '../services/MockData';
import cleanDateValues from '../services/DateService';
import Card from './Card';
import NLPView from './NLPView';

class App extends React.Component {

  backendService = new BackendService();
  mockDataService = new MockDataService();

  mock = false;

  constructor(props) {
    super(props);
    this.state = {
      data: null
    };
    if (this.mock) {
      this.state = {
        data: cleanDateValues(this.mockDataService.getMockViewdata())
      }
    }
  }

  componentDidMount() {
    if (!this.mock) {
      var query = new URLSearchParams(window.location.search);

      this
        .backendService
        .getWebviewData(query.get("token"), query.get("user"))
        .then(result => {
          if (result != null && result.diaryEntries != null && result.moodValues != null) {
            this.setState({ data: cleanDateValues(result), loaded: true });
          } else {
            this.setState({ data: result, loaded: true });
          }
        });
    }
  }

  render() {
    var notEnoughDataWarning = <div></div>;

    if (this.state.data && ((this.state.data.diaryEntries && this.state.data.diaryEntries.length < 3) || (this.state.data.moodValues && this.state.data.moodValues.length < 3))) {
      notEnoughDataWarning = <Card>
        <h1 className="text-yellow-600 text-xl font-semibold">Info: Not many datapoints available.</h1>
        <p>You should use the bot for a couple of days for it to work properly!</p>
      </Card>
    }

    // Default: Loading indicator
    var webview = <div className="flex flex-col min-h-screen">
      <Card>
        <h1 class="text-gray-800 text-4xl font-semibold">Loading...</h1>
        <p>Loading your data - please wait a moment...</p>
      </Card>
    </div>;

    if (this.state.data && this.state.data.diaryEntries && this.state.data.diaryEntries.length > 0) { // Everything alright and loaded

      webview = <div className="flex flex-col min-h-screen">
        <Card>
          <h1 className="text-gray-800 text-4xl font-semibold">Your Mood Diary and Stats</h1>
          <p className="text-yellow-700">You should not share this link with anybody!</p>
        </Card>
        {notEnoughDataWarning}
        <MoodPlot data={this.state.data}></MoodPlot>
        <NLPView data={this.state.data}></NLPView>
        <Diary data={this.state.data}></Diary>
      </div>;

    } else if (this.state.loaded) { // Invalid token case or no data available

      webview = <div className="flex flex-col min-h-screen">
        <Card>
          <h1 className="text-red-700 text-4xl font-semibold">Invalid Link</h1>
          <p>Generate a new one by sending /stats to the Modia bot!</p>
        </Card>
      </div>;

    }

    return (<Router>
      {webview}
    </Router>)
  }
}

export default App;
