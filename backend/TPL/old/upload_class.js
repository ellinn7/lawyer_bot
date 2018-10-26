var Upload = function (etalonDocument, comparedDocument) {
    this.etalonDocument = etalonDocument;
    this.comparedDocument = comparedDocument;
};

Upload.prototype.doUpload = function () {
    var that = this;
    var formData = new FormData();

    // add assoc key values, this will be posts values
    formData.append("etalonDocument", this.etalonDocument, this.etalonDocument.name);
    formData.append("comparedDocument", this.comparedDocument, this.comparedDocument.name);

    $.ajax({
        type: "POST",
        url: "script",
        xhr: function () {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                // Здесь можно добавить визуальные эффекты ожидания
            }
            return myXhr;
        },
        success: function (data) {
            // your callback here
        },
        error: function (error) {
            // handle error
        },
        async: true,
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        timeout: 60000
    });
};