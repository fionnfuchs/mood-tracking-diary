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
        if (previousProps.data != this.props.data && this.props.data != null) {
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


            for (let i = 0; i < this.state.entries.length; i++) {
                entryObjects.push(<h2 class="text-gray-800 text-xl font-semibold">{this.state.dates[i]}</h2>);
                entryObjects.push(<p class="mt-2 text-gray-600">{this.state.entries[i]}</p>);
                entryObjects.push(<p class="mt-2 text-gray-600"></p>);
            }
        }

        return (
            <div class="w-full lg:w-1/2 2xl:w-1/3 py-4 px-8 bg-white shadow-lg rounded-lg my-5">
                <h2 class="text-gray-800 text-2xl font-semibold my-2">Your Diary Entries</h2>
                {entryObjects}
            </div>
        );
    }

}

export default Diary;