import React from 'react';
import Plot from 'react-plotly.js';

class MoodPlot extends React.Component {
    render() {
        return (
            <Plot
                data={[
                    {
                        x: ["22.05.2021", "23.05.2021", "24.05.2021", "25.05.2021", "26.05.2021", "27.05.2021", "28.05.2021"],
                        y: [2, 3, 3, 5, 4, 2, 1],
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