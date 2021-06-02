import React from 'react';

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
        console.log(this.props.data);
        if (previousProps.data != this.props.data && this.props.data != null) {
            this.dataUpdate();
        }
    }

    dataUpdate() {
        console.log("Data is available.");

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


            for (let i = 0; i < this.state.entries.length; i++) {
                entryObjects.push(<p>{this.state.dates[i]}</p>);
                entryObjects.push(<p>{this.state.entries[i]}</p>);
            }
        }

        return (
            <div className="bg-grey-800 text-black rounded-lg border shadow-lg p-5">
                {entryObjects}
            </div>
        );
    }

}

export default Diary;