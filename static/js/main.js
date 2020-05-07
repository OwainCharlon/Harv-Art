var apiEndpointBaseURL = "https://api.harvardartmuseums.org/object";
var queryString = $.param({
    apikey: "b6782a10-8def-11ea-877a-6df674fda82b",
    classification: "Paintings",
    size: "20"
});

function toggleLike() {
    $(".like").toggleClass("liked");
    $(".like").toggleClass("notLiked");
}

// FETCH + CARROUSSEL
let data;
var images = new Array();
var indexCar = 0;
var img1 = 0;
var img2;
var img3;
var img4;
var img5;

$.getJSON(apiEndpointBaseURL + "?" + queryString, function(data) {
    function verifDifImg(img1, img2) {
        if (typeof data.records[img2].images != 'undefined') {
            if (data.records[img1].images[0] === data.records[img2].images[0]) {
                return 0;
            } else { return img2; }
        }
        return 0;
    }
    $(document).ready(function() {
        console.log(data);

        // Tableau pour carrousel
        while (typeof data.records[img1].images[0] === 'undefined') { img1++; }
        images.push("url(\"" + data.records[img1].images[0].baseimageurl);
        img2 = img1 + 1;
        while (verifDifImg(img1, img2) === 0 || typeof data.records[img2].images[0] === 'undefined') { img2++; }
        images.push("url(\"" + data.records[img2].images[0].baseimageurl);
        img3 = img2 + 1;
        while (verifDifImg(img2, img3) === 0 || typeof data.records[img3].images[0] === 'undefined') { img3++; }
        images.push("url(\"" + data.records[img3].images[0].baseimageurl);
        img4 = img3 + 1;
        while (verifDifImg(img3, img4) === 0 || typeof data.records[img4].images[0] === 'undefined') { img4++; }
        images.push("url(\"" + data.records[img4].images[0].baseimageurl);
        img5 = img4 + 1;
        while (verifDifImg(img4, img5) === 0 || typeof data.records[img5].images[0] === 'undefined') { img5++; }
        images.push("url(\"" + data.records[img5].images[0].baseimageurl);
        $('.carrousel').css("background-image", "url(\"" + data.records[img5].images[0].baseimageurl + "\"\)");
        $('.carrousel').fadeOut(2500);
        // Tableau pour Daily Image
        var randomImage = Math.floor(Math.random() * 20);
        while (typeof data.records[randomImage].images[0] === 'undefined' && typeof data.records[randomImage].labeltext === 'undefined') {
            randomImage++;
            if (randomImage > 20) { randomImage = 0; }
        }
        var randomImgUrl = "url(\"" + data.records[randomImage].images[0].baseimageurl + "\"\)";
        var randomImgText = data.records[randomImage].labeltext;
        if (randomImgText == null) {
            randomImgText = "Désolé aucune description n'est renseignée pour cette oeuvre, nous comptons sur la créativité impressionnante de nos internautes pour vous inventer une histoire. Merci <3";
        }
        $('.dailyImg').css("background-image", randomImgUrl);
        $('.dailyDesc p').html(randomImgText);
    });
});

function carrouStyle() {
    setTimeout(() => {
        $('.carrousel').css("background-image", images[indexCar]);
        carrouStyle();
        $('.carrousel').fadeIn(2500);
        $('.carrousel').fadeOut(2500);
        if (indexCar == 4) indexCar = 0;
        indexCar++;
    }, 5000);
}

carrouStyle();

// RESIZE FUNCTION

var headerHeight;
var screenHeight;

function resize() {
    screenHeight = $(window).innerHeight();
    headerHeight = $('.nav').innerHeight() + $('.mainTitle').innerHeight() + 120;
    valueHero = screenHeight - headerHeight;
    $('.containerCarrousel').css('height', valueHero);
}

resize();

$(window).resize(resize);