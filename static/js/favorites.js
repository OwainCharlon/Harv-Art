var ids = new Array();
ids.push($('.favItem'));
//console.log(ids);

ids[0].each(function(index) {
    //console.log(ids[0][index].id);
    var apiEndpointBaseURL = "https://api.harvardartmuseums.org/object";
    var queryString = $.param({
        apikey: "b6782a10-8def-11ea-877a-6df674fda82b"
    });
    $.getJSON(apiEndpointBaseURL + "/" + ids[0][index].id + "?" + queryString, function(data) {
        //console.log(data);
        var id = '\#' + data.objectid;
        element = $(id);
        console.log(element.children());
        element.children()[0].style.backgroundImage = data.images[0].baseimageurl;
        //.css("background-image", "url(\"" + data.images[0].baseimageurl + "\"\)");
        var authorTitle = (data.people) ? (data.title + " - " + data.people[0].name) : (data.title + " - Unknown Artist");
        element.children()[1].children[0]
            //.html(authorTitle);
        var descHis = (data.labeltext) ? (data.labeltext) : ("Aucune description disponible. Déso !");
        element.children()[1].children[1]
            //.html(descHis);
    });
});