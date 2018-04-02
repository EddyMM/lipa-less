function apiCall(url_path, method, data, successCallback, errorCallback) {
    $.ajax({
        url: url_path,
        type: method,
        data: data,
        contentType: 'application/json',
        success: successCallback,
        error: errorCallback
    });
}