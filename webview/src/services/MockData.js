class MockDataService {
    getMockViewdata() {
        return {
            moodValues: [
                {
                    value: 4,
                    timestamp: "2021-06-04T08:54:53.768Z"
                },
                {
                    value: 1,
                    timestamp: "2021-06-05T08:54:53.768Z"
                },
                {
                    value: 5,
                    timestamp: "2021-06-06T08:54:53.768Z"
                },
            ],
            diaryEntries: [
                {
                    entry: "It was a great day.",
                    timestamp: "2021-06-04T08:54:53.768Z"
                },
                {
                    entry: "This is a diary entry.",
                    timestamp: "2021-06-05T08:54:53.768Z"
                },
                {
                    entry: "Lorem ipsum.",
                    timestamp: "2021-06-06T08:54:53.768Z"
                },
            ],
            nlpData: {
                verbs: {
                    "swim": [3, 4, 5, 4, 5, 4],
                    "work": [3, 2, 4, 2, 2],
                    "study": [2]
                },
                nouns: {
                    "university": [2, 3],
                }
            }
        }
    }
}

export default MockDataService;