var interval_id = 0;
function go() {

    clearInterval(interval_id);

    var current_words = [];

    var ticklen = 2000;

    var intervals = [];

    var subset = $('#subset').val();
    
    $.getJSON(subset + '.json', function (data, status, jqXHR) {
        intervals = data;
    });


    var idx = 0;
    function tick() {
        var interval = intervals[idx++];

        $('#datetime').html(interval.date);

        var new_words = [];

        var clusters = interval.clusters;
        for(var c=0; c<clusters.length;c++) {
            for (var k=0; k<clusters[c].length; k++) {
                var id = ("#" + c) + k;
                var word = clusters[c][k];
                new_words.push(word);

                if (current_words.indexOf(word) >= 0)
                {
                    $(id).html('<strong>' + word + '</strong>');
                }
                else
                {
                    $(id).html(word);   
                }

                var isSport = ['nba','nfl','nhl'].indexOf(word) >= 0;
                var color = isSport ? 'red' : 'black';
                $(id).css('color', color);
            }
        }

        current_words = new_words;
    }

    interval_id = setInterval(tick, ticklen);

    $('#subset').on('change', function() {
        go();
    })
}

$(go);