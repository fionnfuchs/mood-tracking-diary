import React from 'react';
import Plot from 'react-plotly.js';
import Card from './Card';

class MoodPlot extends React.Component {

    constructor(props) {
        super(props);
        this.state = { windowWidth: window.innerWidth };

        this.handleResize = this.handleResize.bind(this);
    }

    handleResize(e) {
        this.setState({ windowWidth: window.innerWidth });
    };

    componentDidMount() {
        if (this.props.data && this.props.data.moodValues) {
            this.dataUpdate();
        }
        window.addEventListener("resize", this.handleResize);
    }

    componentDidUpdate(previousProps, previousState) {
        if (previousProps.data !== this.props.data && this.props.data != null) {
            this.dataUpdate();
        }
    }

    componentWillUnmount() {
        window.addEventListener("resize", this.handleResize);
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
                    <Plot style={{ width: "100 %", height: "100 %" }}
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
                            autosize: false,
                            width: Math.min(760, this.state.windowWidth * 0.9),
                            height: Math.min(Math.max(300, this.state.windowWidth * 0.6), 500),
                            plot_bgcolor: "rgba(0,0,0,0)",
                            paper_bgcolor: 'rgba(0,0,0,0)',
                            yaxis: {
                                tickvals: [1, 2, 3, 4, 5],
                                ticktext: ["\u{1F62B} (1)", "\u{1F641} (2)", "\u{1F642} (3)", "\u{1F601} (4)", "\u{1F929} (5)"]
                            }
                        }}
                        useResizeHandler={true} />
                </div>
            </Card>
        );
    }
}

export default MoodPlot;