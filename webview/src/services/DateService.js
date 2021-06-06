function cleanDateValues(data) {
    for (let i = 0; i < data.moodValues.length; i++) {
        let datestring = data.moodValues[i].timestamp;
        datestring = datestring.split("T")[0];
        datestring = datestring.split("-");
        let year = datestring[0];
        let month = datestring[1];
        let day = datestring[2];
        data.moodValues[i].timestamp = day + "." + month + "." + year;
    }
    for (let i = 0; i < data.diaryEntries.length; i++) {
        let datestring = data.diaryEntries[i].timestamp;
        datestring = datestring.split("T")[0];
        datestring = datestring.split("-");
        let year = datestring[0];
        let month = datestring[1];
        let day = datestring[2];
        data.diaryEntries[i].timestamp = day + "." + month + "." + year;
    }
    return data;
}

export default cleanDateValues;