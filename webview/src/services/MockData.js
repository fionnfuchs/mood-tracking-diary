class MockDataService {
    getMockViewdata() {
        return {
            moodValues: [
                {
                    value: 4,
                    timestamp: "01.01.2021"
                },
                {
                    value: 1,
                    timestamp: "02.01.2021"
                },
                {
                    value: 5,
                    timestamp: "03.01.2021"
                },
            ],
            diaryEntries: [
                {
                    entry: "It was a great day.",
                    timestamp: "01.01.2021"
                },
                {
                    entry: "This is a diary entry.",
                    timestamp: "02.01.2021"
                },
                {
                    entry: "Lorem ipsum.",
                    timestamp: "03.01.2021"
                },
            ]
        }
    }
}

export default MockDataService;