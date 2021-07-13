import React from 'react';
import Card from './Card';

class NLPView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {

        let mood_emojis = ["\u{1F62B}", "\u{1F641}", "\u{1F642}", "\u{1F601}", "\u{1F929}"]

        let verbTRs = [];
        let classChange = "";
        for (var verb of Object.keys(this.props.data.nlpData.verbs)) {
            let avg = this.average(this.props.data.nlpData.verbs[verb]);
            verbTRs.push(
                <tr className={classChange + " group select-none"}>
                    <td>{verb}</td>
                    <td>{mood_emojis[Math.round(avg) - 1]} <span className="opacity-20 group-hover:opacity-80">(avg: {avg}, nr: {this.props.data.nlpData.verbs[verb].length}x)</span></td>
                </tr>
            );
            if (classChange == "") {
                classChange = "bg-gray-100";
            } else {
                classChange = "";
            }
        }

        let nounTRs = [];
        classChange = "";
        for (var noun of Object.keys(this.props.data.nlpData.nouns)) {
            let avg = this.average(this.props.data.nlpData.nouns[noun]);
            nounTRs.push(
                <tr className={classChange + " group select-none"}>
                    <td>{noun}</td>
                    <td className="group">{mood_emojis[Math.round(avg) - 1]} <span className="opacity-20 group-hover:opacity-80">(avg: {avg}, nr: {this.props.data.nlpData.nouns[noun].length}x)</span></td>
                </tr>
            );
            if (classChange == "") {
                classChange = "bg-gray-100";
            } else {
                classChange = "";
            }
        }


        return (
            <Card>
                <h2 className="text-gray-800 text-2xl font-semibold">NLP Data</h2>
                <h2 className="text-gray-800 text-xl font-semibold">Verbs</h2>
                <div className="container p-4">
                    <table className="w-full bg-white">
                        <thead className="bg-gray-200">
                            <tr>
                                <th className="w-1/2 text-left">Verb</th>
                                <th className="w-1/2 text-left">Average Mood</th>
                            </tr>
                        </thead>
                        <tbody>
                            {verbTRs}
                        </tbody>
                    </table>
                </div>
                <h2 className="text-gray-800 text-xl font-semibold">Nouns</h2>
                <div class="container p-4">
                    <table class="w-full bg-white">
                        <thead className="bg-gray-200">
                            <tr>
                                <th className="w-1/2 text-left">Noun</th>
                                <th className="w-1/2 text-left">Average Mood</th>
                            </tr>
                        </thead>
                        <tbody>
                            {nounTRs}
                        </tbody>
                    </table>
                </div>
            </Card>
        );
    }

    average(array) {
        var sum = 0;
        for (var value of array) {
            if (typeof (value) != "number") {
                sum += parseInt(value);
            }
            else {
                sum += value;
            }
        }
        return this.roundToOneDec(sum / array.length);
    }

    roundToOneDec(num) {
        return Math.round(num * 10) / 10;
    }
}

export default NLPView;