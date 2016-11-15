function trimDailyErrs(rangeErrDict) {
    var newErrList = new Array();
    for (var i in rangeErrDict) {
        if (parseFloat(rangeErrDict[i]) > 0.5) {
            newErrList.push('0.5');
        } else {
            newErrList.push(rangeErrDict[i]);
        }
    }
    return newErrList;
}
