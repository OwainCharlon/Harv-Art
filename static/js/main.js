var apiEndpointBaseURL = "https://api.harvardartmuseums.org/object";
var queryString = $.param({
    apikey: "b6782a10-8def-11ea-877a-6df674fda82b",
    classification: "Paintings",
    size: "15",
    hasimage: "1"
});

function toggleLike() {
    $(".fsLike").toggleClass("liked");
    $(".fsLike").toggleClass("notLiked");
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
        //console.log(data);

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
        //console.log(images);


        // Tableau pour Daily Image

        var randomImage = Math.floor(Math.random() * 15);
        while (typeof data.records[randomImage].images[0] === 'undefined' && typeof data.records[randomImage].labeltext === 'undefined') {
            randomImage++;
            if (randomImage > 15) { randomImage = 0; }
        }
        var randomId = data.records[randomImage].id
        var randomImgUrl = "url(\"" + data.records[randomImage].images[0].baseimageurl + "\"\)";
        var randomImgText = data.records[randomImage].labeltext;
        if (randomImgText == null) {
            randomImgText = "Désolé aucune description n'est renseignée pour cette oeuvre, nous comptons sur la créativité impressionnante de nos internautes pour vous inventer une histoire. Merci <3";
        }
        $('.dailyImg').attr('id', randomId);
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
    headerHeight = $('.navbar').innerHeight() + $('.mainTitle').innerHeight() + 200;
    valueCarrou = screenHeight - headerHeight;
    $('.containerCarrousel').css('height', valueCarrou);
}

resize();

$(window).resize(resize);

// Sign in en pop up

function signIn() {
    $('.overlay').css('display', 'block');
    $('.signInSection').css('display', 'flex');
}

function closeSignInAndCo() {
    $('.overlay').css('display', 'none');
    $('.signInSection').css('display', 'none');
    $('.bigImg').css('display', 'none');
    $('.fsAuthorTitle').empty();
    $('.fsDesc').empty();
    $('.fsComment').empty();
}

// On récupère les Id des masterpieces et on les mets dans les Div pour bosser propre

function fetchImgInfo(imgId) {
    var apiEndpointBaseURL = "https://api.harvardartmuseums.org/object";
    var queryString = $.param({
        apikey: "b6782a10-8def-11ea-877a-6df674fda82b"
    });

    $.getJSON(apiEndpointBaseURL + "/" + imgId + "?" + queryString, function(data) {
        $(document).ready(function() {
            console.log(data);

            var authorTitle = (data.people) ? (data.title + " - " + data.people[0].name) : (data.title + " - Unknown Artist");
            $('.fsAuthorTitle').append(authorTitle);
            var img = "url(\"" + data.images[0].baseimageurl + "\"\)";
            $('.fsImg').css("background-image", img);
            var desc = (data.labeltext) ? (data.labeltext) : ("Aucune description disponible. Déso !");
            $('.fsDesc').append(desc);


            var getComments = jQuery.ajax({
                type: 'GET',
                url: window.origin + '/getComments' + '/' + imgId,
                dataType: 'JSON',

                success: function(code_html, statut) {
                    console.log("Masterpiece comments well returned");
                },

                error: function(resultat, statut, erreur) {
                    console.log("Ajax error while returning masterpiece comments.");
                },
                complete: function(resultat, statut) {
                    console.log(resultat.responseJSON);
                    comments = resultat.responseJSON;
                    for (const element of comments) {
                        elements = element.split(',');
                        $('.fsComment').append("<div class=\"comment\"><div class=\"comAuthor\">" + elements[2] + " - " + elements[1] + "</div><div class=\"comText\">" + elements[0] + "</div></div>");
                    }
                }
            });

            var addHistory = jQuery.ajax({
                type: 'GET',
                url: window.origin + '/addContent' + '/' + 2 + '/' + imgId,
                dataType: 'JSON',
    
                success: function(code_html, statut) {
                    console.log("Well added to your history.");
                },
    
                error: function(resultat, statut, erreur) {
                    console.log("Can not add it to your history.");
                },
                complete: function(resultat, statut) {
                }
            });
        });

        $('#addComment').click(function(){
            var addComment = jQuery.ajax({
                type: 'GET',
                url: window.origin + '/addContent' + '/' + 3 + '/' + imgId + '/' + $('input[name=inputComment]').val(),
                dataType: 'JSON',

                success: function(code_html, statut) {
                    console.log("Well added to comments.");
                },

                error: function(resultat, statut, erreur) {
                    console.log("Can not add it to comments.");
                },
                complete: function(resultat, statut) {
                }
            });
        });
    });

    $('#addFavorite').click(function(){
        var addFavorite = jQuery.ajax({
            type: 'GET',
            url: window.origin + '/addContent' + '/' + 1 + '/' + imgId,
            dataType: 'JSON',

            success: function(code_html, statut) {
                console.log("Well added to your favorite.");
            },

            error: function(resultat, statut, erreur) {
                console.log("Can not add it to your favorite.");
            },
            complete: function(resultat, statut) {
            }
        });
    });
}

// Faire ressortir l'image au clic

function imgFS(imgId) {
    $('.overlay').css('display', 'block');
    $('.bigImg').css('display', 'grid');
    fetchImgInfo(imgId);
}


// ATTENTION VIDER CONTENU HTML QUAND OVERLAY CLICKé