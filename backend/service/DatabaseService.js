class DatabaseService {
    connect(url = "mongodb://mongodb:27017/") {
        const mongoClient = require('mongodb').MongoClient;
        const _service = this;

        mongoClient.connect(url, function (err, db) {
            _service.userDatabase = db.db("userdata");
        });
    }

    async getWebViewData(token, userid) {
        if (await this.accessTokenValid(token, userid)) {
            const diaryEntries = await this.getDiaryEntries(userid);
            const moodValues = await this.getMoodValues(userid);
            const nlpValues = await this.getNlpValues(userid);
            console.log({ "diaryEntries": diaryEntries, "moodValues": moodValues, "nlpData": nlpValues[0] });
            return { "diaryEntries": diaryEntries, "moodValues": moodValues, "nlpData": nlpValues[0] };
        }

    }

    async getNlpValues(userid) {
        const nlpCollection = this.userDatabase.collection("nlp_analysis");
        const cursor = nlpCollection.find({ userid: parseInt(userid) });

        if ((await cursor.count()) === 0) {
            console.log("No NLP Analysis found!");
        }

        var entries = [];

        entries = await cursor.toArray();
        return entries;
    }

    async accessTokenValid(token, userid) {
        const accessTokenCollection = this.userDatabase.collection("access_tokens");

        const cursor = accessTokenCollection.find({ userid: parseInt(userid), token: token })
        const token_available = await cursor.count()
        if (token_available > 0) {
            console.log("Valid token...");
            return true;
        } else {
            console.log("Invalid token...");
            return false;
        }
    }

    async getDiaryEntries(userid) {
        const diaryEntryCollection = this.userDatabase.collection("diary_entries");
        const cursor = diaryEntryCollection.find({ userid: parseInt(userid) }).sort({ timestamp: -1 });

        if ((await cursor.count()) === 0) {
            console.log("No documents found!");
        }

        var entries = [];

        entries = await cursor.toArray();
        return entries;
    }

    async getMoodValues(userid) {
        const moodValueCollection = this.userDatabase.collection("mood_value");
        const cursor = moodValueCollection.find({ userid: parseInt(userid) }).sort({ timestamp: 1 });

        if ((await cursor.count()) === 0) {
            console.log("No documents found!");
        }

        var entries = [];

        entries = await cursor.toArray();
        return entries;
    }
}

exports.DatabaseService = DatabaseService;