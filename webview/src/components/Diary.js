import React from 'react';
import Card from './Card';

class Diary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        if (this.props.data && this.props.data.diaryEntries) {
            this.dataUpdate();
        }
    }

    componentDidUpdate(previousProps, previousState) {
        if (previousProps.data !== this.props.data && this.props.data != null) {
            this.dataUpdate();
        }
    }

    dataUpdate() {
        var entries = [];
        var dates = [];
        for (var value of this.props.data.diaryEntries) {
            entries.push(value.entry);
            dates.push(value.timestamp);
        }

        this.setState({ entries: entries, dates: dates });
        console.log(this.state);
    }

    render() {

        if (this.state && this.state.entries) {
            var entryObjects = [];

            let entryDict = {};
            console.log(entryDict);
            for (let i = 0; i < this.state.entries.length; i++) {
                let date = this.state.dates[i];
                if (entryDict[date] == undefined) {
                    entryDict[date] = [this.state.entries[i]];
                }
                else {
                    entryDict[date].push(this.state.entries[i]);
                }

            }

            for (var date of Object.keys(entryDict)) {
                entryObjects.push(
                    <h2 className="text-gray-800 text-xl font-semibold">{"\u{1F4D6} "}{date}</h2>
                );
                for (var entry of entryDict[date]) {
                    entryObjects.push(<p className="mt-2 text-gray-600">{
                        entry
                    }</p>);
                }
                entryObjects.push(<p className="mt-2 text-gray-600"></p>);
            }
        }


        return (
            <Card>
                <h2 className="text-gray-800 text-2xl font-semibold my-2">Your Diary Entries</h2>
                {entryObjects}
            </Card >
        );
    }

}

export default Diary;