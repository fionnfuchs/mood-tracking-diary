var express = require('express');


function viewRoute(databaseService) {
  var router = express.Router();
  router.get('/', async (req, res, next) => {
    res.send('respond with a view');
    var diaryEntries = await databaseService.getDiaryEntries("1219933767");
    console.log(diaryEntries);
  });
  return router;
}


module.exports.viewRoute = viewRoute;
