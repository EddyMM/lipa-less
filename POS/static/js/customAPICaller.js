function apiCall(url_path, data, successCallback, errorCallback) {
    $.ajax({
        url: url_path,
        type: 'POST',
        data: data,
        contentType: 'application/json',
        success: successCallback,
        error: errorCallback
    });
}