import React from 'react';
import Plot from 'react-plotly.js';

class MoodPlot extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};

    }

    componentDidMount() {
        if (this.props.data && this.props.data.moodValues) {
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

        var moodValues = [];
        var dates = [];
        for (var value of this.props.data.moodValues) {
            moodValues.push(value.value);
            dates.push(value.timestamp);
        }

        this.setState({ values: moodValues, dates: dates });
    }

    render() {
        return (
            <Plot
                data={[
                    {
                        x: this.state.dates,
                        y: this.state.values,
                        type: 'scatter',
                        mode: 'lines+markers',
                        marker: { color: 'purple' },
                    },
                ]}
                config={
                    { staticPlot: true }
                }
                layout={{ width: 600, height: 400, title: 'Your mood last week', plot_bgcolor: "rgba(0,0,0,0)", paper_bgcolor: 'rgba(0,0,0,0)' }}
            />
        );
    }
}

export default MoodPlot;