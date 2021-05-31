var express = require('express');


function viewRoute(databaseService) {
  var router = express.Router();
  router.get('/', async (req, res, next) => {

    const user = req.query.user;
    const token = req.query.token;

    console.log("Trying to get view data for user " + user + " with token " + token);
    const viewData = await databaseService.getWebViewData(user, token);
    console.log(viewData);

    res.send(viewData);

  });
  return router;
}


module.exports.viewRoute = viewRoute;
