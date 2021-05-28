class DatabaseService {
    connect(url = "mongodb://mongodb:27017/") {
        const mongoClient = require('mongodb').MongoClient;
        const _service = this;

        mongoClient.connect(url, function (err, db) {
            _service.userDatabase = db.db("userdata");
        });
    }

    async getDiaryEntries(userid) {
        const diaryEntryCollection = this.userDatabase.collection("diary_entries");
        const cursor = diaryEntryCollection.find({ userid: parseInt(userid) });

        if ((await cursor.count()) === 0) {
            console.log("No documents found!");
        }

        var entries = [];

        entries = await cursor.toArray();
        return entries;
    }
}

exports.DatabaseService = DatabaseService;