import React from 'react';
import Plot from 'react-plotly.js';
import Card from './Card';

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
        if (previousProps.data !== this.props.data && this.props.data != null) {
            this.dataUpdate();
        }
    }

    dataUpdate() {
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
            <Card>
                <h2 className="text-gray-800 text-2xl font-semibold">Your Mood Stats</h2>
                <div className="flex items-center justify-center">
                    <Plot
                        data={[{
                            x: this.state.dates,
                            y: this.state.values,
                            type: 'scatter',
                            mode: 'lines+markers',
                            marker: {
                                color: 'purple'
                            }
                        }
                        ]}
                        config={{
                            staticPlot: true
                        }}
                        layout={{
                            width: 600,
                            height: 400,
                            plot_bgcolor: "rgba(0,0,0,0)",
                            paper_bgcolor: 'rgba(0,0,0,0)'
                        }} />
                </div>
            </Card>
        );
    }
}

export default MoodPlot;