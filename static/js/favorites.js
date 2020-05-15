function toggleLikeFav() {
    $(".like").toggleClass("liked");
    $(".like").toggleClass("notLiked");
}


// Récupérer les ID
// Faire un fetch des id et stocker URL et description et autre
// boucler pour append chaque div

// var ids = new Array();
// $(".favItem").siblings().attr('id');

var totalFav = $(".listFav").children().length - 1;

var i = 0;
var y = 0;
var favID = new Array();

while (i < totalFav) {
    favID.push($(".listFav").children()[i].id);
    i++;
}

while (y < favID.length) {
    // Ca fait pas ce que je veux, cherche ducon
    $.getJSON("https://api.harvardartmuseums.org/object?relatedto=" + /*favID[y]*/ "219512" + "&apikey=b6782a10-8def-11ea-877a-6df674fda82b", function(data) {
        console.log(data);
    });
    y++;
}

console.log(favID);

//$('.listFav').append('<div class="favItem" class=classe>Coucou</div>');