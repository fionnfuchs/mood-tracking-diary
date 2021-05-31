var express = require('express');


function viewRoute(databaseService) {
  var router = express.Router();
  router.get('/', async (req, res, next) => {
    const user = req.query.user;
    const token = req.query.token;
    console.log("Trying to get view data for user " + user + " with token " + token);
    var diaryEntries = await databaseService.getWebViewData(user, token);
    console.log(diaryEntries);
    res.send(diaryEntries);
  });
  return router;
}


module.exports.viewRoute = viewRoute;
