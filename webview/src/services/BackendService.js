import CONFIG from "../config";

class BackendService {

    async getWebviewData(token, userid) {
        var data = null;
        try {
            data = await fetch(CONFIG.BACKENDURL + "/api/view?user=" + userid + "&token=" + token).then(response => response.json());
        } catch (err) {
            data = null;
        }
        return data;
    }

}

export default BackendService;