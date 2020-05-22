var ids = new Array();
ids.push($('.favItem'));
var idLength = ids[0].length;
// console.log(i);
console.log(ids);
var favBackgrd = new Array();
var apiEndpointBaseURL = "https://api.harvardartmuseums.org/object";
var queryString = $.param({
    apikey: "b6782a10-8def-11ea-877a-6df674fda82b"
});

// var y = 0;
// while (y < idLength) {
//     $.getJSON(apiEndpointBaseURL + "/" + ids[0][y].id + "?" + queryString, function(data) {
//         //console.log(data);
//         var backgrd = "url(\"" + data.images[0].baseimageurl + "\");";
//         favBackgrd.push(backgrd);
//         //console.log(backgrd);
//     });
//     y++;
// }

// console.log(favBackgrd);

// var z = 0;
// while (z < idLength) {
//     var element = ids[0][z];
//     //console.log($(element));
//     var elementChild = $(element).children();
//     console.log(z);
//     console.log(favBackgrd[z]);
//     $(elementChild[0])[0].style.backgroundImage = favBackgrd[z];
//     console.log($(elementChild[0])[0].style.backgroundImage);
//     z++;
// }


function getBkgnd(ids, favBackgrd) {
    return new Promise(function(resolve, reject) {
        var y = 0;
        while (y < idLength) {
            $.getJSON(apiEndpointBaseURL + "/" + ids[0][y].id + "?" + queryString, function(data) {
                //console.log(data);
                var backgrd = "url(\"" + data.images[0].baseimageurl + "\");";
                favBackgrd.push(backgrd);
                console.log("premier While");
            });
            y++;
        }
    }).then(function() {
        var z = 0;
        while (z < idLength) {
            var element = ids[0][z];
            console.log("deuxieme While");
            var elementChild = $(element).children();
            console.log(z);
            console.log(favBackgrd[z]);
            $(elementChild[0])[0].style.backgroundImage = favBackgrd[z];
            console.log($(elementChild[0])[0].style.backgroundImage);
            z++;
        }
    });
};

getBkgnd();

// ids[0].each(function(index) {
//     //console.log(ids[0][index].id);
//     var apiEndpointBaseURL = "https://api.harvardartmuseums.org/object";
//     var queryString = $.param({
//         apikey: "b6782a10-8def-11ea-877a-6df674fda82b"
//     });
//     $.getJSON(apiEndpointBaseURL + "/" + ids[0][index].id + "?" + queryString, function(data) {
//         console.log(data);
//         // var id = '\#' + data.objectid;
//         // element = $(id);
//         //console.log(ids[index].children);
//         // element.children()[0].style.backgroundImage = data.images[0].baseimageurl;
//         // //.css("background-image", "url(\"" + data.images[0].baseimageurl + "\"\)");
//         // var authorTitle = (data.people) ? (data.title + " - " + data.people[0].name) : (data.title + " - Unknown Artist");
//         // element.children()[1].children[0]
//         //     //.html(authorTitle);
//         // var descHis = (data.labeltext) ? (data.labeltext) : ("Aucune description disponible. Déso !");
//         // element.children()[1].children[1]
//         //     //.html(descHis);
//     });
// });