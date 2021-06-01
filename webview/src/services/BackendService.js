import CONFIG from "../config";

class BackendService {

    async getWebviewData(token, userid) {
        const data = await fetch(CONFIG.BACKENDURL + "/api/view?user=" + userid + "&token=" + token).then(response => response.json());
        return data;
    }

}

export default BackendService;